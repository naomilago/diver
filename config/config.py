from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.json'],
)

if __name__ == '__main__':
    print('')
    print('\nProject:')
    print('- Name:', settings.project.name)
    print('- Description:', settings.project.description)

    print('\nDeveloper:')
    print('- Name:', settings.people.developer.name)
    print('')