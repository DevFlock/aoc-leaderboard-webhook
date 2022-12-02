# AoC Private Leaderboard Discord Webhook

Sends/updates a leaderboard in a discord chat of your choosing! Updates every 30 (changable) minutes. If you do change the time, please don't go below 15 minutes to not spam AoC's servers :)



## Setup
Create an ENV file in the root directory with these values:

```env
SESSION_COOKIE=
WEBHOOK_URL=
LEADERBOARD_URL=
MESSAGE_ID=
```

`SESSION_COOKIE`: Your AoC session cookie<br>
`WEBHOOK_URL`: The url to the discord webhook<br>
`LEADERBOARD_URL`: The url to the AoC private leaderboard<br>
`MESSAGE_ID`: (Optional) The id of the message to be edited instead. Note that the a message has had to be sent using the same webhook url

