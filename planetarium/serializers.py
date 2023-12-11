from rest_framework import serializers

from planetarium.models import ShowTheme, AstronomyShow


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes = serializers.StringRelatedField(many=True, read_only=True)
