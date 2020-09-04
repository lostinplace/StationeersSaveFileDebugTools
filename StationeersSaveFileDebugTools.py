import click



@click.group()
def cli():
    pass

@cli.command("restore_atmo")
@click.argument('currentFile')
@click.argument('backupFile')
@click.argument('newFilePath')
def restore_atmo(current_file, backup_file, new_file_path):
    from .Utils.RestoreAtmo import create_restored_world_file
    create_restored_world_file(current_file, backup_file, new_file_path)


if __name__ == '__main__':
    cli()