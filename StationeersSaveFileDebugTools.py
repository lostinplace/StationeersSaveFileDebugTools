import click



@click.group()
def cli():
    pass

@cli.command("restore_atmo")
@click.argument('currentFile')
@click.argument('backupFile')
@click.argument('newFilePath')
def restore_atmo(current_file, backup_file, new_file_path):
    from Utils.AtmoFileProcessing.RestoreAtmo import create_restored_world_file
    create_restored_world_file(current_file, backup_file, new_file_path)


@cli.command("generate_start_condition")
@click.argument('world')
def generate_start_condition(world):
    from Utils.StartConditionProcessing.StartConditionGenerator import convert_world_file_to_startconditions
    out = convert_world_file_to_startconditions(world)
    print(out)


if __name__ == '__main__':
    cli()