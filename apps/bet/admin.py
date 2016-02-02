from django.contrib import admin
from django.utils.html import format_html
from models import (Better, Song, Bet, BetItem, Artist,
                    Week, Position)


class PositionAdmin(admin.ModelAdmin):
    list_filter = ('week',)


class SongAdmin(admin.ModelAdmin):
    def show_youtube_link(self, obj):
        return format_html(
            """<a href='https://www.youtube.com/watch?v={url}'>
            https://www.youtube.com/watch?v={url}</a>""",
            url=obj.youtube_link)

    fieldsets = (
        (None, {
            'fields': ('name', 'show_youtube_link', 'youtube_link', 'artist', 'artist_name')
        }),
    )
    readonly_fields = ('show_youtube_link',)


admin.site.register(Better)
admin.site.register(Song, SongAdmin)
admin.site.register(Bet)
admin.site.register(BetItem)
admin.site.register(Artist)
admin.site.register(Week)
admin.site.register(Position, PositionAdmin)
