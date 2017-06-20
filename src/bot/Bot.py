import discord
from connect4.Game import Game
from connect4.AI import KearneyOne
import copy

import bot.Config as Config

client = discord.Client()

games = {}
colors = {}

ai_player = KearneyOne.KearneyOneAI()


async def change_color(message):
    ind = message.content.find("#")
    if ind > -1:
        color = message.content[ind:]
        colors[message.author] = color
    else:
        await client.send_message(message.channel, "Colors must be set as hex")


async def resign(message):
    try:
        game_info = games[message.author.id]
    except KeyError:
        await client.send_message(message.channel, "You are not currently in a game " + message.author.mention)
        return

    opp_id = game_info['opponent'].id

    del games[opp_id]
    del games[message.author.id]

    await client.send_message(message.channel, message.author.mention + " resigned")


async def start_game(message):
    player = message.author
    opponent = message.mentions[0]

    if player in games or opponent in games:
        await client.send_message(message.channel, "One of you is already in another game!")
        return

    game = Game()
    games[player.id] = {'game': game, 'opponent': opponent, "team": 0, "AI": False}
    games[opponent.id] = {'game': game, 'opponent': player, "team": 1, "AI": False}

    if opponent == client.user:
        print("But it was me, Dio!")
        games[opponent.id]["AI"] = True

    # await client.send_message(message.channel, "`" + str(games[message.author]['game']) + "`")

    file_name = "temp/" + str(player.id) + ".png"

    game.generate_image_board().save(file_name, "PNG")

    await client.send_file(message.channel, file_name)


async def make_move(message):
    column = message.content[-1]
    try:
        game_info = games[message.author.id]
    except KeyError:
        await client.send_message(message.channel, "You are not currently in a game " + message.author.mention)
        return
    if game_info['game'].get_turn() == game_info['team']:
        if column.isdigit() and 0 <= int(column) < 7 and game_info['game'].move(int(column)):
            if game_info['game'].check_win():
                file_name = "temp/" + str(message.author.id) + ".png"

                render_board(message.author.id, file_name)

                await client.send_file(message.channel, file_name, content=message.author.mention + " won!")

                end_game(message.author.id)

            else:
                file_name = "temp/" + str(message.author.id) + ".png"
                render_board(message.author.id, file_name)

                sent = await client.send_file(message.channel, file_name)

                if games[game_info["opponent"].id]["AI"]:
                    await client.edit_message(sent, new_content="AI is thinking...")
                    ai_move = ai_player.get_move(copy.copy(game_info["game"].board))
                    content = "AI chose column " + str(ai_move)
                    game_info["game"].move(ai_move)

                    render_board(game_info["opponent"].id, file_name)

                    if game_info["game"].check_win():
                        content += ". The AI won!"
                        end_game(game_info["opponent"].id)

                    await client.delete_message(sent)

                    await client.send_file(message.channel, file_name, content=content)
        else:
            await client.send_message(message.channel, "You must give a valid column " + message.author.mention)
    else:
        await client.send_message(message.channel, "It is not your turn " + message.author.mention)


def end_game(aut_id):
    game_info = games[aut_id]
    opp_id = game_info['opponent'].id

    del games[opp_id]
    del games[aut_id]


def render_board(aut_id, file_name):
    if games[aut_id]["team"] == 0:
        pc = colors.get(aut_id, "red")
        oc = colors.get(games[aut_id]['opponent'], "black")
        games[aut_id]['game'].generate_image_board(pc, oc).save(file_name, "PNG")
    else:
        pc = colors.get(aut_id, "black")
        oc = colors.get(games[aut_id]['opponent'], "red")
        games[aut_id]['game'].generate_image_board(oc, pc).save(file_name, "PNG")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith("!c4"):
        if message.content.startswith("!c4 color"):
            await change_color(message)
        elif message.content == "!c4 resign":
            await resign(message)
        elif message.content.startswith('!c4 start'):
            await start_game(message)
        elif message.content.startswith('!c4 move'):
            await make_move(message)


client.run(Config.TOKEN)
