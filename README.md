# Message deleter

Creative name, I know.

A Discord selfbot that deletes messages from select users or channels, with a live-reloadable and configurable allow/deny list, without explicitly banning them.

Perfect for removing messages from users deemed annoying, without sending a message, so to speak.

Obviously you need permissions to manage messages from users. And not get caught in audit log (optional).

## Installation

OS is assumed to be Linux. 

```
git clone https://github.com/EquinoxAlpha/mdeleter
cd mdeleter
python -m venv .
soource ./bin/activate
pip install -r requirements.txt
```

## Running

```
TOKEN=yourtoken python main.py
```

Obviously you need to replace yourtoken with your Discord account's token. Doing this will be left as an exercise for the reader.

## Configuration

Check `deny.json` for an example on how to configure the allow/deny lists. `allow.json` has the same format as `deny.json`. Allow directives have higher priority than deny directives. Some basic wildcards are supported (nothing advanced like you would expect in a shell though).

Users, guilds, and channels are specified by their ID. Users and channels can be wildcards, and for allow directives, guilds can be wildcards too.

## Disclaimer

Discord selfbots are against Discord's Terms of Service. But let's be honest, if you're reading this, you probably don't care, and I don't care either.

That being said, I'm not responsible if your Discord account gets terminated. Good luck and happy deleting.