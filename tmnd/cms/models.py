from datetime import datetime

from dateutil.parser import parse
from loguru import logger

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    OneToOneField,
)

from tmnd.cms import spotify


class Member(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    spotify_refresh_token = CharField(max_length=1024)
    member_spotify_id = CharField(max_length=128, unique=True)
    playlist_spotify_id = CharField(max_length=128, unique=True, null=True)

    def __str__(self):
        return self.member_spotify_id

    @property
    def profile_url(self):
        url = f"https://open.spotify.com/user/{self.member_spotify_id}"
        return url

    @property
    def sp(self):
        return spotify.auth(self.member_spotify_id, self.spotify_refresh_token)

    def create_playlist(self):
        if self.playlist_spotify_id is not None:
            raise ValueError("Playlist already exists", self)

        sp_playlist = spotify.create_playlist(self.member_spotify_id, self.sp)
        self.playlist_spotify_id = sp_playlist["id"]
        self.save()

    def update_playlist(self):
        # fetch all liked tracks
        liked_tracks = spotify.fetch_saved_tracks(self.member_spotify_id, self.sp)
        liked_track_ids = [track["track"]["id"] for track in liked_tracks]

        # delete imported tracks not in liked
        existing_track_ids = self.track_set.values_list("track_spotify_id", flat=True)
        for existing_track_id in existing_track_ids:
            if existing_track_id not in liked_track_ids:
                Track.objects.get(
                    member=self,
                    track_spotify_id=existing_track_id,
                ).delete()

        # add newly liked tracks
        for liked_track in liked_tracks:
            added_at = parse(liked_track["added_at"])
            track, created = Track.objects.get_or_create(
                member=self,
                track_spotify_id=liked_track["track"]["id"],
                defaults={"added": added_at},
            )
            if created:
                track.added = added_at
                track.save()

        # update playlist with newly liked tracks
        spotify.update_playlist(
            self.member_spotify_id,
            self.sp,
            self.playlist_spotify_id,
            liked_track_ids,
        )


class Track(Model):
    member = ForeignKey(Member, on_delete=CASCADE)
    track_spotify_id = CharField(max_length=128)
    added = DateTimeField()

    def __str__(self):
        return f"{self.track_spotify_id} [{self.member}]"

    @property
    def track_embed_url(self):
        url = f"https://open.spotify.com/embed/track/{self.track_spotify_id}"
        return url
