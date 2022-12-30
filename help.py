from rich.console import Console

console = Console()

console.print('\nTo run a command: [bold]make [blue]command[/blue][/bold]')

with open('makefile', 'r', encoding='UTF-8') as file:
    for line in file:
        if line.find('##') >= 0:
            if line.find('@') >= 0:
                section = line.split('@')[-1].strip().capitalize()
                console.print(f'\n{section}', style='bold green', end='\n\n')
            else:
                partials = line.split('##')
                command = partials[0].split(':')[0].strip().capitalize()
                description = partials[-1].strip().capitalize()
                console.print(
                    f'[bold][blue]{command}[/blue]:[/bold] {description}'
                )
