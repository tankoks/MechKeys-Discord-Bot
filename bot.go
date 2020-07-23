package main

import (
	"context"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/andersfylling/disgord"
	"github.com/andersfylling/disgord/std"
	"github.com/andersfylling/snowflake"
)

func main() {
	client, err := disgord.NewClient(disgord.Config{
		BotToken: os.Getenv("DISGORD_TOKEN"),
		CacheConfig: &disgord.CacheConfig{
			Mutable:                  false,
			DisableUserCaching:       false,
			UserCacheLifetime:        time.Duration(4) * time.Hour,
			DisableVoiceStateCaching: true,
			DisableChannelCaching:    false,
			ChannelCacheLifetime:     0,
		},
	})

	if err != nil {
		return
	}

	defer client.StayConnectedUntilInterrupted(context.Background())

	client.On(disgord.EvtMessageCreate, verify)

	client.On(disgord.EvtMessageCreate, regionRoles)

	voteFilter, _ := std.NewMsgFilter(context.Background(), client)
	voteFilter.SetPrefix("!vote")
	client.On(disgord.EvtMessageCreate, voteFilter.NotByBot, voteFilter.HasPrefix, vote)

	lifealertFilter, _ := std.NewMsgFilter(context.Background(), client)
	lifealertFilter.SetPrefix("!lifealert")
	client.On(disgord.EvtMessageCreate, lifealertFilter.NotByBot, lifealertFilter.HasPrefix, lifealert)

	purgeFilter, _ := std.NewMsgFilter(context.Background(), client)
	purgeFilter.SetPrefix("!purge")
	client.On(disgord.EvtMessageCreate, purgeFilter.NotByBot, purgeFilter.HasPrefix, purgeFilter.StripPrefix, purge)

	tradeFilter, _ := std.NewMsgFilter(context.Background(), client)
	tradeFilter.SetPrefix("!trade")
	client.On(disgord.EvtMessageCreate, tradeFilter.NotByBot, tradeFilter.HasPrefix, tradeFilter.StripPrefix, trade)
}

func verify(session disgord.Session, evt *disgord.MessageCreate) {
	msg := evt.Message
	verifyChannel := disgord.NewSnowflake(256281609878110208)
	verifyRole := disgord.NewSnowflake(256281441078345752)

	if msg.ChannelID == verifyChannel {
		if msg.Content == "ripster55 is a shitposter" {
			_ = session.AddGuildMemberRole(context.Background(), msg.GuildID, msg.Author.ID, verifyRole)
		}
		session.DeleteMessage(context.Background(), msg.ChannelID, msg.ID)
	}
}

func regionRoles(session disgord.Session, evt *disgord.MessageCreate) {
	msg := evt.Message

	regionChannel := disgord.NewSnowflake(317737076160331786)

	var roles = map[string]uint64{
		"!NA":     317376486640189440,
		"!AUS":    317376875183996929,
		"!EU":     317376455627636736,
		"!SEA":    317376733340762114,
		"!SA":     317376594127749120,
		"!AFRICA": 317376721655562240,
		"!ASIA":   317376869638864927,
		"!ME":     317389130671718400,
		"!CANADA": 552639100088221697,
	}

	if msg.ChannelID == regionChannel {
		if val, ok := roles[msg.Content]; ok {
			_ = session.AddGuildMemberRole(context.Background(), msg.GuildID, msg.Author.ID, disgord.NewSnowflake(val))
		}
		session.DeleteMessage(context.Background(), msg.ChannelID, msg.ID)
	}
}

func vote(session disgord.Session, evt *disgord.MessageCreate) {
	msg := evt.Message
	msg.React(context.Background(), session, "👍")
	msg.React(context.Background(), session, "👎")
}

func lifealert(session disgord.Session, evt *disgord.MessageCreate) {
	msg := evt.Message
	channel, _ := session.GetChannel(context.Background(), msg.ChannelID)
	response, _ := msg.Reply(context.Background(), session, "LifeAlert Recieved")
	modChannel := disgord.NewSnowflake(325265301958557696)

	embed := disgord.Embed{
		Title:     "Life Alert",
		Color:     0xff0000,
		Timestamp: disgord.Time{},
		Fields: []*disgord.EmbedField{
			&disgord.EmbedField{
				Name:   "Author",
				Value:  msg.Author.Mention(),
				Inline: true,
			},
			&disgord.EmbedField{
				Name:   "User ID",
				Value:  msg.Author.ID.String(),
				Inline: true,
			},
			&disgord.EmbedField{
				Name:   "Channel",
				Value:  channel.Mention(),
				Inline: false,
			},
			&disgord.EmbedField{
				Name:   "Time",
				Value:  msg.Timestamp.String(),
				Inline: true,
			},
			&disgord.EmbedField{
				Name:   "Message",
				Value:  msg.Content,
				Inline: false,
			},
			&disgord.EmbedField{
				Name: "Jump To Chat",
				Value: fmt.Sprintf("https://discordapp.com/channels/%s/%s/%s",
					msg.GuildID.String(),
					msg.ChannelID.String(),
					response.ID.String()),
				Inline: false,
			},
		},
	}

	session.SendMsg(context.Background(), modChannel, "@here", embed)
	session.DeleteMessage(context.Background(), msg.ChannelID, msg.ID)
}

func purge(session disgord.Session, evt *disgord.MessageCreate) {
	msg := evt.Message

	for _, n := range msg.Member.Roles {
		if n == snowflake.NewSnowflake(387703313283416085) || n == snowflake.NewSnowflake(190330163743948800) {
			numString := strings.Replace(msg.Content, " ", "", -1)
			num, err := strconv.ParseUint(numString, 10, 32)

			if err != nil {
				return
			}

			uintnum := uint(num)

			messages, err := session.GetMessages(context.Background(), msg.ChannelID, &disgord.GetMessagesParams{
				Before: msg.ID,
				Limit:  uintnum,
			})

			if err != nil {
				return
			}

			deletemessages := []snowflake.Snowflake{}

			for _, message := range messages {
				deletemessages = append(deletemessages, message.ID)
			}

			session.DeleteMessages(context.Background(), msg.ChannelID, &disgord.DeleteMessagesParams{Messages: deletemessages})
			session.DeleteMessage(context.Background(), msg.ChannelID, msg.ID)
			msg.Reply(context.Background(), session, "👀")
			break
		}
	}
}

func trade(session disgord.Session, evt *disgord.MessageCreate) {
	msg := evt.Message
	msg.Reply(context.Background(), session, `This is a reminder that this discord SHOULD NOT be used as a trading platform. We have no way of preventing scammers from utilizing this service and we have no way to verify trades or crosscheck the scammer list. Exercise caution if you do trade with other members of the discord, and remember to always use Paypal "Goods and Services" or equivalent. Trade with users here at your own risk.`)
}
