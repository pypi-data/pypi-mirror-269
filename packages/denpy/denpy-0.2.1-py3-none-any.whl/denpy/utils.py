import discord
from rich.table import Table
from rich.console import Console
from json import load
import inspect
import psutil


def create_table(params, values):
    table = Table()
    for param, value in zip(params, values):
        table.add_column(param)
    table.add_row(*values)
    console = Console()
    console.print(table)


def get_ram_usage():
    return f'{round(psutil.virtual_memory().used / 10000000)} MB'


async def send_custom_message(id, channel: discord.TextChannel or discord.DMChannel, view=None, variables=None, edit: discord.Message or discord.Interaction = False):
    if variables is None:
        variables = {}
    path = inspect.stack()[1].filename.replace('\\', '/').split('/')
    path.pop(-1)
    path.pop(-1)
    with open(f'{"/".join(path)}/embeds/{id}.json', 'r', encoding='utf-8') as file:
        config = load(file)

    embeds = []
    for embed_ in config['embeds']:
        embed = discord.Embed(
            title=embed_.get('title'),
            description=embed_.get('description'),
            color=embed_['color']
        )
        if 'image' in embed_:
            embed.set_image(url=embed_['image']['url'])
        if 'thumbnail' in embed_:
            embed.set_thumbnail(url=embed_['thumbnail']['url'])
        if 'fields' in embed_:
            for field in embed_['fields']:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        embeds.append(embed)

    for variable in variables:
        config['content'] = config['content'].replace(f'{variable}', str(variables[variable])) if config['content'] is not None else None
        for embed in embeds:
            embed.title = embed.title.replace(f'{variable}', str(variables[variable])) if embed.title is not None else None
            embed.description = embed.description.replace(f'{variable}', str(variables[variable])) if embed.description is not None else None
            for field in embed.fields:
                field.name = field.name.replace(f'{variable}', str(variables[variable])) if field.name is not None else None
                field.value = field.value.replace(f'{variable}', str(variables[variable])) if field.value is not None else None

    if edit is False:
        message = await channel.send(content=config['content'], embeds=embeds, view=view)
    else:
        if discord.message.Message == type(edit):
            message = await edit.edit(content=config['content'], embeds=embeds, view=view)
        else:
            message = await edit.response.edit_message(content=config['content'], embeds=embeds, view=view)
    return message
