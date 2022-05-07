import argparse
import os
import sys

from pycraft.level import Level


def parse_args():
    parser = argparse.ArgumentParser(description='Take a census of the user\'s region')
    parser.add_argument('--world', '-w', type=str, help='Path to saved world', default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.world is None:
        world = os.environ.get('WORLDPATH')
    else:
        world = args.world

    if world is None:
        print(f'World not specified')
        sys.exit(1)
    level = Level(os.path.join(world, 'level.dat'))
    def print_all(level):
        print(f'WanderingTraderSpawnChance: {level.WanderingTraderSpawnChance}')
        print(f'       BorderCenterZ: {level.BorderCenterZ}')
        print(f'          Difficulty: {level.Difficulty}')
        print(f'  BorderSizeLerpTime: {level.BorderSizeLerpTime}')
        print(f'             raining: {level.raining}')
        print(f'                Time: {level.Time}')
        print(f'            GameType: {level.GameType}')
        print(f'        ServerBrands: {level.ServerBrands}')
        print(f'       BorderCenterX: {level.BorderCenterX}')
        print(f'BorderDamagePerBlock: {level.BorderDamagePerBlock}')
        print(f' BorderWarningBlocks: {level.BorderWarningBlocks}')
        print(f'    WorldGenSettings: {level.WorldGenSettings}')
        print(f'         DragonFight: {level.DragonFight}')
        print(f'BorderSizeLerpTarget: {level.BorderSizeLerpTarget}')
        print(f'             Version: {level.Version}')
        print(f'             DayTime: {level.DayTime}')
        print(f'         initialized: {level.initialized}')
        print(f'           WasModded: {level.WasModded}')
        print(f'       allowCommands: {level.allowCommands}')
        print(f'WanderingTraderSpawnDelay: {level.WanderingTraderSpawnDelay}')
        print(f'    CustomBossEvents: {level.CustomBossEvents}')
        print(f'           GameRules: {level.GameRules}')
        print(f'              Player: {level.Player}')
        print(f'              SpawnY: {level.SpawnY}')
        print(f'            rainTime: {level.rainTime}')
        print(f'         thunderTime: {level.thunderTime}')
        print(f'              SpawnZ: {level.SpawnZ}')
        print(f'            hardcore: {level.hardcore}')
        print(f'   WanderingTraderId: {level.WanderingTraderId}')
        print(f'    DifficultyLocked: {level.DifficultyLocked}')
        print(f'              SpawnX: {level.SpawnX}')
        print(f'    clearWeatherTime: {level.clearWeatherTime}')
        print(f'          thundering: {level.thundering}')
        print(f'          SpawnAngle: {level.SpawnAngle}')
        print(f'             version: {level.version}')
        print(f'      BorderSafeZone: {level.BorderSafeZone}')
        print(f'          LastPlayed: {level.LastPlayed}')
        print(f'   BorderWarningTime: {level.BorderWarningTime}')
        print(f'     ScheduledEvents: {level.ScheduledEvents}')
        print(f'           LevelName: {level.LevelName}')
        print(f'          BorderSize: {level.BorderSize}')
        print(f'         DataVersion: {level.DataVersion}')
        print(f'           DataPacks: {level.DataPacks}')
    # level.dump()
    print_all(level)