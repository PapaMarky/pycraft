from pycraft import DatFile


class Level(DatFile):
    """
    Level.dat data.
    """

    def __init__(self, path: str):
        """
        Create an instance of Level. See https://minecraft.fandom.com/wiki/Java_Edition_level_format

        :param path: Path to the saved world
        """
        super().__init__(path)

    @property
    def allowCommands(self):
        """
        1 or 0 (true/false) - true if cheats are enabled.
        """
        return self._tags['Data']['allowCommands'].value

    @property
    def BorderCenterX(self):
        """
        Center of the world border on the X coordinate. Defaults to 0.
        """
        return self._tags['Data']['BorderCenterX'].value

    @property
    def BorderCenterZ(self):
        """
        Center of the world border on the Z coordinate. Defaults to 0.
        """
        return self._tags['Data']['BorderCenterZ'].value

    @property
    def BorderDamagePerBlock(self):
        """
        Defaults to 0.2.
        """
        return self._tags['Data']['BorderDamagePerBlock'].value

    @property
    def BorderSize(self):
        """
        Width and length of the border of the border. Defaults to 60000000.
        """
        return self._tags['Data']['BorderSize'].value

    @property
    def BorderSafeZone(self):
        """
        Defaults to 5.
        """
        return self._tags['Data']['BorderSafeZone'].value

    @property
    def BorderSizeLerpTarget(self):
        """
        Defaults to 60000000.
        """
        return self._tags['Data']['BorderSizeLerpTarget'].value

    @property
    def BorderSizeLerpTime(self):
        """
        Defaults to 0.
        """
        return self._tags['Data']['BorderSizeLerpTime'].value

    @property
    def BorderWarningBlocks(self):
        """
        Defaults to 5.
        """
        return self._tags['Data']['BorderWarningBlocks'].value

    @property
    def BorderWarningTime(self):
        """
        Defaults to 15.
        """
        return self._tags['Data']['BorderWarningTime'].value

    @property
    def clearWeatherTime(self):
        """
        The number of ticks until "clear weather" has ended.
        """
        return self._tags['Data']['clearWeatherTime'].value

    @property
    def CustomBossEvents(self):
        """
        A collection of bossbars.
        """
        return self._tags['Data']['CustomBossEvents'].value

    @property
    def DataPacks(self):
        """
        Options for datapacks.
        """
        return self._tags['Data']['DataPacks'].value

    @property
    def DataVersion(self):
        """
        An integer displaying the data version.
        """
        return self._tags['Data']['DataVersion'].value

    @property
    def DayTime(self):
        """
        The time of day. 0 is sunrise, 6000 is mid day, 12000 is sunset, 18000 is mid night, 24000 is the next day's 0.
        This value keeps counting past 24000 and does not reset to 0.
        """
        return self._tags['Data']['DayTime'].value

    @property
    def Difficulty(self):
        """
        The current difficulty setting. 0 is Peaceful, 1 is Easy, 2 is Normal, and 3 is Hard. Defaults to 2.
        """
        return self._tags['Data']['Difficulty'].value

    @property
    def DifficultyLocked(self):
        """
        1 or 0 (true/false) - True if the difficulty has been locked. Defaults to 0.
        """
        return self._tags['Data']['DifficultyLocked'].value

    @property
    def GameRules(self):
        """
        The gamerules used in the world.
        """
        return self._tags['Data']['GameRules'].value

    @property
    def WorldGenSettings(self):
        """
        Used in 1.16, the generation settings for each dimension.
        """
        return self._tags['Data']['WorldGenSettings'].value

    @property
    def GameType(self):
        """
        The default game mode for the singleplayer player when they initially spawn.
        0 is Survival, 1 is Creative, 2 is Adventure, 3 is Spectator.
        Note: Singleplayer worlds do not use this field to save which game mode the player is currently in.
        """
        return self._tags['Data']['GameType'].value

    @property
    def hardcore(self):
        """
        1 or 0 (true/false) - true if the player will respawn in Spectator on death in singleplayer.
        Affects all three game modes.
        """
        return self._tags['Data']['hardcore'].value

    @property
    def initialized(self):
        """
        1 or 0 (true/false) - Normally true after a world has been initialized properly after creation.
        If the initial simulation was canceled somehow, this can be false and the world will be re-initialized
        on next load.
        """
        return self._tags['Data']['initialized'].value

    @property
    def LastPlayed(self):
        """
        The Unix time in milliseconds when the level was last loaded.
        """
        return self._tags['Data']['LastPlayed'].value

    @property
    def LevelName(self):
        """
        The name of the level.
        """
        return self._tags['Data']['LevelName'].value

    @property
    def Player(self):
        """
        he state of the Singleplayer player. This overrides the <player>.dat file with the same name as the
        Singleplayer player. This is only saved by Servers if it already exists, otherwise it is not saved for
        server worlds. See Player.dat Format. (https://minecraft.fandom.com/wiki/Player.dat_format#NBT_Structure)
        """
        return self._tags['Data']['Player'].value

    @property
    def raining(self):
        """
        1 or 0 (true/false) - true if the level is currently experiencing rain, snow, and cloud cover.
        """
        return self._tags['Data']['raining'].value

    @property
    def rainTime(self):
        """
        The number of ticks before "raining" is toggled and this value gets set to another random value.
        """
        return self._tags['Data']['rainTime'].value

    @property
    def SpawnX(self):
        """
        The X coordinate of the world spawn.
        """
        return self._tags['Data']['SpawnX'].value

    @property
    def SpawnY(self):
        """
        The Y coordinate of the world spawn.
        """
        return self._tags['Data']['SpawnY'].value

    @property
    def SpawnZ(self):
        """
        The Z coordinate of the world spawn.
        """
        return self._tags['Data']['SpawnZ'].value

    @property
    def thundering(self):
        """
        1 or 0 (true/false) - true if the rain/snow/cloud cover is a lightning storm and dark enough for mobs to
        spawn under the sky.
        """
        return self._tags['Data']['thundering'].value

    @property
    def thunderTime(self):
        """
        The number of ticks before "thundering" is toggled and this value gets set to another random value.
        """
        return self._tags['Data']['thunderTime'].value

    @property
    def Time(self):
        """
        The number of ticks since the start of the level.
        """
        return self._tags['Data']['Time'].value

    @property
    def version(self):
        """
        The NBT version of the level, with 1.14.4 being 19133.
        """
        return self._tags['Data']['version'].value

    @property
    def Version(self):
        """
        Information about the Minecraft version the world was saved in.

        Id: An integer displaying the data version.
        Name: The version name as a string, e.g. "15w32b".
        Series: Developing series. In 1.18 experimental snapshots, it was set to "ccpreview". In others, set to "main".
        Snapshot: 1 or 0 (true/false) – Whether the version is a snapshot or not.
        """
        return self._tags['Data']['Version'].value

    @property
    def WanderingTraderId(self):
        """
        The UUID of the current wandering trader in the world saved as four ints.
        """
        return self._tags['Data']['WanderingTraderId'].value

    @property
    def WanderingTraderSpawnChance(self):
        """
        The current chance of the wandering trader spawning next attempt; this value is the percentage and will be
        divided by 10 when loaded by the game, for example a value of 50 means 5.0% chance.
        """
        return self._tags['Data']['WanderingTraderSpawnChance'].value

    @property
    def WanderingTraderSpawnDelay(self):
        """
        The amount of ticks until another wandering trader is attempted to spawn
        """
        return self._tags['Data']['WanderingTraderSpawnDelay'].value

    @property
    def WasModded(self):
        """
        1 or 0 (true/false) - true if the world was opened in a modified version.
        """
        return self._tags['Data']['WasModded'].value

    @property
    def DragonFight(self):
        """
        Data for the ender dragon fight. Only appears after the end is entered.
        """
        return self._tags['Data']['DragonFight'].value

    @property
    def ServerBrands(self):
        return self._tags['Data']['ServerBrands'].value

    @property
    def SpawnAngle(self):
        return self._tags['Data']['SpawnAngle'].value

    @property
    def ScheduledEvents(self):
        return self._tags['Data']['ScheduledEvents'].value
