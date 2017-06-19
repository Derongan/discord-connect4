import discord
import asyncio
from connect4.Game import Game
from io import BytesIO
from PIL import Image

import bot.Config as Config

client = discord.Client()

games = {}
colors = {}


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
            ind = message.content.find("#")
            if ind > -1:
                color = message.content[ind:]
                colors[message.author] = color
            else:
                await client.send_message(message.channel, "Colors must be set as hex")

        elif message.content == "!c4 resign":
            try:
                game_info = games[message.author.id]
            except KeyError:
                await client.send_message(message.channel, "You are not currently in a game " + message.author.mention)

            opp_id = game_info['opponent'].id

            del games[opp_id]
            del games[message.author.id]


        elif message.content.startswith('!c4 start'):
            player = message.author
            opponent = message.mentions[0]

            if player in games or opponent in games:
                await client.send_message(message.channel, "One of you is already in another game!")
                return

            game = Game()
            games[player.id] = {'game': game, 'opponent': opponent, "team": 0}
            games[opponent.id] = {'game': game, 'opponent': player, "team": 1}
            # await client.send_message(message.channel, "`" + str(games[message.author]['game']) + "`")

            file_name = "temp/" + str(player.id) + ".png"

            game.generate_image_board().save(file_name, "PNG")

            await client.send_file(message.channel, file_name)

        elif message.content.startswith('!c4 move'):
            column = message.content[-1]
            try:
                game_info = games[message.author.id]
            except KeyError:
                await client.send_message(message.channel, "You are not currently in a game " + message.author.mention)
                return
            if game_info['game'].turn == game_info['team']:
                if column.isdigit() and int(column) >= 0 and int(column) < 7:
                    winner = game_info['game'].move(int(column))
                    if winner == -1:
                        await client.send_message(message.channel,
                                                  "You must give a valid column " + message.author.mention)
                    elif winner:
                        file_name = "temp/" + str(message.author.id) + ".png"

                        if game_info["team"] == 0:
                            pc = colors.get(message.author, "red")
                            oc = colors.get(game_info['opponent'], "black")
                            game_info['game'].generate_image_board(pc, oc).save(file_name, "PNG")
                        else:
                            pc = colors.get(message.author, "black")
                            oc = colors.get(game_info['opponent'], "red")
                            game_info['game'].generate_image_board(oc, pc).save(file_name, "PNG")

                        await client.send_file(message.channel, file_name, content=message.author.mention + " won!")

                        opp_id = game_info['opponent'].id

                        del games[opp_id]
                        del games[message.author.id]

                    else:
                        file_name = "temp/" + str(message.author.id) + ".png"

                        if game_info["team"] == 0:
                            pc = colors.get(message.author, "red")
                            oc = colors.get(game_info['opponent'], "black")
                            game_info['game'].generate_image_board(pc, oc).save(file_name, "PNG")
                        else:
                            pc = colors.get(message.author, "black")
                            oc = colors.get(game_info['opponent'], "red")
                            game_info['game'].generate_image_board(oc, pc).save(file_name, "PNG")

                        await client.send_file(message.channel, file_name)
                else:
                    await client.send_message(message.channel, "You must give a valid column " + message.author.mention)
            else:
                await client.send_message(message.channel, "It is not your turn " + message.author.mention)


client.run(Config.TOKEN)
