# blackjack minigame

import discord
from discord.ext import commands
import helper as h
import time
from collections import defaultdict


class Blackjack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # the actual blackjack game
    @commands.command()
    # only one instance of blackjack can be running per channel at a time
    @commands.cooldown(1, 3600, commands.BucketType.channel)
    async def blackjack(self, ctx, *names: discord.Member):
        # get the bots avatar url for usage via embed messages
        url = self.bot.user.avatar_url
        # various embed messages to be used later in regards to spelling errors / game events
        spell_error1 = discord.Embed(title="Error ❌", color=0xfffafa)
        spell_error1.add_field(name="Start or Stop Command not Recognized...",
                               value="*$blackjack is case-sensitive. Check your spelling and try again*")
        spell_error2 = discord.Embed(title="Error ❌", color=0xfffafa)
        spell_error2.add_field(name="Hit or Stand Command not Recognized...",
                               value="*$blackjack is case-sensitive. check your spelling and try again*")
        spell_error3 = discord.Embed(title="Error ❌", color=0xfffafa)
        spell_error3.add_field(name="yes or no Command not Recognized...",
                               value="*$blackjack is case-sensitive. check your spelling and try again*")
        stop_game = discord.Embed(title="Thanks for Playing! 🃏", color=0xfffafa)
        stop_game.set_footer(text="developed by goose#4609 · $creator",
                             icon_url="https://cdn.discordapp.com/avatars/"
                                      "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
        # the main loop the game runs inside of
        while True:
            # check the max player limit is not reached, if it is send an error message and return
            if len(names) > 6:
                too_many = discord.Embed(title="Error ❌", color=0xfffafa)
                too_many.add_field(name="Too Many Players...",
                                   value="*$blackjack currenlty supports a maximum of 6 players*")
                too_many.set_footer(text="developed by goose#4609 · $creator",
                                    icon_url="https://cdn.discordapp.com/avatars/"
                                             "293658485210480640/f417d959fbe4306240cbecb6a985198a.png?size=1024")
                await ctx.send(embed=too_many)
                await self.blackjack.reset_cooldown(ctx)
                return
            # check that player names were given
            if len(names) == 0:
                no_names = discord.Embed(title="Error ❌", color=0xff7b00)
                no_names.add_field(name="No Player Names Found", value="$blackjack requires player names to be included"
                                                                       " after the command.\n"
                                                                       "*example: $blackjack name name etc.*")
                no_names.set_footer(text="developed by goose#4609 · $creator",
                                    icon_url="https://cdn.discordapp.com/avatars/"
                                             "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
                await ctx.send(embed=no_names)
                await self.blackjack.reset_cooldown(ctx)
                return

            # a list representing six decks worth of cards, shuffled
            card_decks = h.shuffle_cards()
            # a list representing the above decks card values
            card_values = h.value_order(card_decks)

            # list of the dealers cards in string form
            dealer_cards = []
            # list of the dealers card values
            dealer_total = []
            # list of the players cards in string form
            player_cards = defaultdict(list)
            # list of the players card values
            player_total = defaultdict(list)
            # used for indexing the card order in the shufled deck
            deck_walker = 0
            # used for indexing the dealers cards after the deal
            dealer_walker = 2
            # counting the number of busts
            bust_count = 0

            # various tracker objects for the players in the game to be used later
            members = []
            member_ids = []
            player_display_names = []
            player_count = 0
            for name in names:
                members.append(name)
                player_display_names.append(name.display_name)
                player_count += 1
            player_names = ""
            count = 1
            for name in player_display_names:
                player_names += "{}.".format(count)
                player_names += " {}\n".format(name)
                count += 1
            for mem in members:
                member_ids.append(str(mem.id))
            seen = []
            for name in player_display_names:
                if name not in seen:
                    seen.append(name)

            # check if the same player has two hands (one per table, per player)
            if len(seen) != len(player_display_names):
                embed = discord.Embed(title="Error ❌", color=0xfffafa)
                embed.add_field(name="Only one hand per user...", value="*$blackjack only supports one hand per user.*")
                embed.set_footer(text="developed by goose#4609 · $creator",
                                 icon_url="https://cdn.discordapp.com/avatars/"
                                          "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
                await ctx.send(embed=embed)
                await self.blackjack.reset_cooldown(ctx)
                return

            # send a message that the game is about to begin
            deal = discord.Embed(title="Dealing cards...", color=0xfffafa)
            await ctx.send(embed=deal)

            # deal cards to the player(s)
            for n in range(2):
                for name in player_display_names:
                    player_cards[name].append(card_decks[deck_walker])
                    player_total[name].append(int(card_values[deck_walker]))
                    deck_walker += 1
            # dealers turn to be dealt two cards
            dealer_cards.append(card_decks[deck_walker])
            dealer_total.append(int(card_values[deck_walker]))
            deck_walker += 1
            dealer_cards.append(card_decks[deck_walker])
            dealer_total.append(int(card_values[deck_walker]))
            deck_walker += 1

            # get the dealers possible hand combinations using a helper function
            dealer_combos = h.possible_hands(dealer_total)

            # init the table via embed to be updated and sent in chat throughout the game
            table = discord.Embed(title="Current Table 🃏", color=0xfffafa)

            # show the dealers first card, leaving the second one hidden and update the table
            # check for an ace which can be worth either 1 or 11 in blackjack
            if dealer_combos[0] != dealer_combos[1] and dealer_combos[0] == 1:
                table.add_field(name="The Dealer (1 or 11)", value="{}\ncard hidden".format(dealer_cards[0]),
                                inline=False)
            elif dealer_combos[0] != dealer_combos[1] and dealer_total[0] == 1:
                table.add_field(name="The Dealer (1 or 11)", value="{}\ncard hidden"
                                .format(dealer_cards[0]), inline=False)
            # when there is no ace off the deal for the dealer
            else:
                table.add_field(name="The Dealer ({})".format(dealer_total[0]), value="{}\ncard hidden"
                                .format(dealer_cards[0]), inline=False)

            # update the table with the players cards
            for name in player_display_names:
                p_crds = player_total[name]
                player_combos = h.possible_hands(p_crds)
                # if the player has an ace off the deal
                if player_combos[0] != player_combos[1] and player_combos[1] != 21:
                    table.add_field(name="{} ({} or {})".format(name, player_combos[0],
                                                                player_combos[1]),
                                    value="{}\n{}".format(player_cards[name][0],
                                                          player_cards[name][1]))
                # else the player does not have an ace off the deal
                else:
                    table.add_field(name="{} ({})".format(name, player_combos[1]),
                                    value="{}\n{}".format(player_cards[name][0],
                                                          player_cards[name][1]))

            # a slight delay between the dealing cards message and the table being sent
            time.sleep(2.5)
            await ctx.send(embed=table)

            # a variable used for editing the dealers cards on the table as more get added
            dealer_string = "{}\n{}\n".format(dealer_cards[0], dealer_cards[1])

            # indexing variables
            name_index = 0
            t_index = 1
            # when this index gets increased by 1, it acts as the player finishing their turn
            i = 0

            # this loop handles all of the players moves
            # once a player either reaches 21, stands, or busts
            # a break line is reached and it becomes the next players turn
            while i < player_count:
                def player_status(m):
                    # possible responses from the player once prompted
                    if "hit" in m.content.lower() and m.author in members:
                        return "hit"
                    elif "stand" in m.content.lower() and m.author in members:
                        return "stand"
                    elif "stop" in m.content.lower() and m.author in members:
                        return 1
                    # likely a user spelling error
                    elif m.author in members:
                        return -1

                name = player_display_names[name_index]
                p_crds = []
                # find the player combos for the player being prompted
                for val in player_total[name]:
                    p_crds.append(val)

                # fetch the players possible hand combinations
                player_combos = h.possible_hands(p_crds)

                # string to be used in updating cards on the table for the players
                hit_string = ""
                for card in player_cards[name]:
                    hit_string += "{}\n".format(card)

                # auto-stand message
                auto = discord.Embed(title="{} auto-stood on 21".format(name), color=0xfffafa)

                # auto-stand if the player has a natural blackjack off of the deal
                if player_combos[1] == 21:
                    table.remove_field(t_index)
                    hit_string += "*blackjack!*"
                    table.insert_field_at(t_index, name="{} ({})".format(player_display_names[name_index],
                                                                         player_combos[1]),
                                          value=hit_string)

                    await ctx.send(embed=auto)
                    i += 1
                    t_index += 1
                    if name == player_display_names[-1]:
                        await ctx.send(embed=table)
                        # move on to the next player
                        break
                    else:
                        name_index += 1

                # embed message for prompting the player and their move
                q = discord.Embed(color=0xfffafa)
                q.add_field(name="{}, What Would you Like to do? 🃏".format(player_display_names[name_index]),
                            value="1. Hit\n"
                                  "2. Stand\n")
                await ctx.send(embed=q)

                # the players message sent in a text channel to be read by the bot
                msg = await self.bot.wait_for('message', check=player_status)

                # determine what the player decided
                if msg:
                    # stop the game (kill switch)
                    if player_status(msg) == 1:
                        await ctx.send(embed=stop_game)
                        await self.blackjack.reset_cooldown(ctx)
                        return
                    # spelling error (bot did not recognize the players input)
                    elif player_status(msg) == -1:
                        await ctx.send(embed=spell_error2)
                    # player elects to hit
                    elif player_status(msg) == "hit":
                        # add the drawn card to the players two card trackers (face and value)
                        player_cards[name].append(card_decks[deck_walker])
                        player_total[name].append(int(card_values[deck_walker]))
                        # display the drawn card to the table
                        hit_string = ""
                        for card in player_cards[name]:
                            hit_string += "{}\n".format(card)
                        # adjusts the affected walkers after a hit
                        deck_walker += 1
                        # re-determine the players possible hand
                        p_crds = []
                        for val in player_total[name]:
                            p_crds.append(val)
                        player_combos = h.possible_hands(p_crds)
                        # remove the players cards on the table
                        table.remove_field(t_index)
                        # if the players hit causes them to bust
                        if player_combos[0] == -1:
                            # add the players last drawn card to the table
                            hit_string += "*you busted.*"
                            table.insert_field_at(t_index, name="{} ({})".format(player_display_names[name_index],
                                                                                 player_combos[1]),
                                                  value=hit_string)
                            await ctx.send(embed=table)
                            name_index += 1
                            t_index += 1
                            i += 1
                            bust_count += 1
                        # if the players hit results in a blackjack
                        elif player_combos[1] == 21:
                            hit_string += "*blackjack!*"
                            table.insert_field_at(t_index, name="{} ({})".format(player_display_names[name_index],
                                                                                 player_combos[1]),
                                                  value=hit_string)

                            await ctx.send(embed=table)
                            i += 1
                            name_index += 1
                            t_index += 1
                        # if the player has an ace that can still be high
                        elif player_combos[0] != player_combos[1]:
                            # add the players last drawn card to the table and update their total
                            table.insert_field_at(t_index, name="{} ({} or {})".format(player_display_names[name_index],
                                                                                       player_combos[0],
                                                                                       player_combos[1]),
                                                  value=hit_string)
                            await ctx.send(embed=table)
                        # if the player has zero aces or an ace that can only count as 1
                        else:
                            table.insert_field_at(t_index, name="{} ({})".format(player_display_names[name_index],
                                                                                 player_combos[1]),
                                                  value=hit_string)
                            await ctx.send(embed=table)
                    # if the player elects to stand
                    elif player_status(msg) == "stand":
                        hit_string = ""
                        for card in player_cards[name]:
                            hit_string += "{}\n".format(card)
                        hit_string += "*stand*"
                        table.remove_field(t_index)
                        table.insert_field_at(t_index, name="{} ({})".format(player_display_names[name_index],
                                                                             player_combos[1]),
                                              value=hit_string)
                        await ctx.send(embed=table)
                        i += 1
                        name_index += 1
                        t_index += 1

            # this if block is skipped when every player busts, since the dealer does not hit in this case
            if bust_count != len(player_display_names):
                # send a message showing the dealer flipping their face-down card
                dealer_msg = discord.Embed(title="The Dealer is flipping their hidden card... 🃏",
                                           color=0xfffafa)
                await ctx.send(embed=dealer_msg)

                # dealers turn to either hit or stand
                # check what move the dealer needs to make
                if dealer_combos[1] > 16 and dealer_combos[1] != 21:
                    # in this case the dealer would stand
                    table.remove_field(0)
                    dealer_string += "*stand.*"
                    table.insert_field_at(0, name="The Dealer ({})".format(dealer_combos[1]),
                                          value=dealer_string, inline=False)
                    table.add_field(name="** **", value="*generating results...*", inline=False)
                    time.sleep(2)
                    await ctx.send(embed=table)
                elif dealer_combos[1] != 21:
                    table.remove_field(0)
                    if dealer_combos[0] == dealer_combos[1] or dealer_combos[1] == 21:
                        table.insert_field_at(0, name="The Dealer ({})".format(dealer_combos[1]),
                                              value=dealer_string, inline=False)
                    else:
                        # if the dealer has an ace that makes their total one of two values
                        table.insert_field_at(0, name="The Dealer ({} or {})".format(dealer_combos[0],
                                                                                     dealer_combos[1]),
                                              value=dealer_string, inline=False)
                    time.sleep(2.5)
                    await ctx.send(embed=table)

                hit_check = False
                # if the dealer has to hit
                while dealer_combos[1] < 17:
                    hit_check = True
                    # draw a card for the dealer
                    dealer_cards.append(card_decks[deck_walker])
                    dealer_total.append(int(card_values[deck_walker]))
                    # update the dealers hand on the table
                    dealer_string += "{}\n".format(dealer_cards[dealer_walker])
                    # update the dealers possible hand combinations
                    dealer_combos = h.possible_hands(dealer_total)
                    # move the walkers
                    deck_walker += 1
                    dealer_walker += 1

                    if dealer_combos[1] > 21:
                        # remove the dealers hand from the table
                        table.remove_field(0)
                        dealer_string += "*bust.*"
                        table.insert_field_at(0, name="The Dealer ({})".format(dealer_combos[1]),
                                              value=dealer_string, inline=False)
                    elif dealer_combos[1] > 16 and dealer_combos[1] != 21:
                        # remove the dealers hand from the table
                        table.remove_field(0)
                        dealer_string += "*stand.*"
                        table.insert_field_at(0, name="The Dealer ({})".format(dealer_combos[1]),
                                              value=dealer_string, inline=False)

                # if the dealer has a blackjack
                if dealer_combos[1] == 21:
                    table.remove_field(0)
                    if hit_check:
                        dealer_msg = discord.Embed(title="The Dealer is hitting... 🃏",
                                                   color=0xfffafa)
                        await ctx.send(embed=dealer_msg)
                    dealer_string += "*blackjack!*"
                    table.insert_field_at(0, name="The Dealer ({})".format(dealer_combos[1]),
                                          value=dealer_string,
                                          inline=False)
                    table.add_field(name="** **", value="*generating results...*", inline=False)
                    time.sleep(2.5)
                    await ctx.send(embed=table)
                elif hit_check:
                    dealer_msg = discord.Embed(title="The Dealer is hitting... 🃏",
                                               color=0xfffafa)
                    await ctx.send(embed=dealer_msg)
                    table.add_field(name="** **", value="*generating results...*", inline=False)

                    time.sleep(2.5)
                    await ctx.send(embed=table)

            # create a new embed message for hand results
            results = discord.Embed(color=0xfffafa)
            if bust_count != len(player_display_names):
                # the three possible dealer outcomes
                if dealer_combos[1] > 21:
                    results.add_field(name="Hand Results 🃏", value="*The Dealer busted.*", inline=False)
                elif dealer_combos[1] == 21:
                    results.add_field(name="Hand Results 🃏", value="*The Dealer got a blackjack!*", inline=False)
                else:
                    results.add_field(name="Hand Results 🃏", value="*The Dealer stood on {}*".format(dealer_combos[1]),
                                      inline=False)
            else:
                # this procs if every player in the game busted, and skips the dealer hitting message from sending
                # to match real blackjack rules
                if len(player_display_names) == 1:
                    results.add_field(name="Hand Results 🃏", value="*you busted.*", inline=False)
                elif bust_count == len(player_display_names):
                    results.add_field(name="Hand Results 🃏", value="*every hand busted.*", inline=False)

            # include the bots profile picture in the results message
            results.set_thumbnail(url=url)

            # this loop checks each player against the dealer and updates the results message
            for name in player_display_names:
                p_crds = []
                for val in player_total[name]:
                    p_crds.append(val)
                # fetch player combinations
                player_combos = h.possible_hands(p_crds)
                # compare against the dealer
                game_status = h.check_winner(player_combos, dealer_combos)
                if game_status == "d_win":
                    # the dealer wins
                    results.add_field(name="{}".format(name),
                                      value="*You lost.*")
                    i += 1
                elif game_status == "push":
                    # the player and dealer tie
                    results.add_field(name="{}".format(name),
                                      value="*You pushed.*")
                    i += 1
                elif game_status == "p_win":
                    # the player wins
                    if player_combos[1] < 22:
                        results.add_field(name="{}".format(name),
                                          value="*You won!*")
                        i += 1
                    # in the case where a helper function thinks the player won, but both they and the
                    # dealer actually busted
                    else:
                        results.add_field(name="{}".format(name),
                                          value="*You lost.*")
                        i += 1

            time.sleep(2.5)
            # ask the table if they would like to play another hand (appears at the bottom of the results msg)
            results.add_field(name="Play Another Hand?", value="*yes / no*", inline=False)
            # send the results message
            await ctx.send(embed=results)

            while True:
                # function determines if the table would like to play another hand
                def play_again(m):
                    if "yes" in m.content.lower() and m.author in members:
                        return "yes"
                    elif "no" in m.content.lower() and m.author in members:
                        return "no"
                    elif m.author in members:
                        return -1

                msg = await self.bot.wait_for('message', check=play_again)
                if msg:
                    if play_again(msg) == "yes":
                        break
                    elif play_again(msg) == "no":
                        await ctx.send(embed=stop_game)
                        await self.blackjack.reset_cooldown(ctx)
                        return
                    else:
                        await ctx.send(embed=spell_error3)
            # re-starts the first while loop, thus creating a brand new game
            continue

    # blackjack command error handler
    @blackjack.error
    async def blackjack_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            # procs if a name argument could not be found inside the Discord server
            embed = discord.Embed(title="Error ❌", color=0xff7b00)
            embed.add_field(name="One of the Given Players Could not be Found...",
                            value="$blackjack is case-sensitive. Check your spelling")
            embed.set_footer(text="developed by goose#4609 · $creator",
                             icon_url="https://cdn.discordapp.com/avatars/"
                                      "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
            await ctx.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(Blackjack(bot))
