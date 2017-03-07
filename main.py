from flask import Flask, render_template, url_for, redirect, request
from steamapi import core, user, store


app = Flask("Steamer")
core.APIConnection(api_key="97EBFD00E4237E4C049D0EAE5A80ADCC")


@app.route('/post/profile/', methods=['POST'])
def set_profile():

    if request.method == 'POST':
        name = request.form['profile_name']
    else:
        name = ''
    return redirect(url_for('view_profile', name=name))


@app.route('/user/view/<name>/', methods=['GET', 'POST'])
def view_profile(name=None):
    try:
        try:

            steam_user = user.SteamUser(userid=int(name))
        except ValueError:  # Not an ID, but a vanity URL.

            steam_user = user.SteamUser(userurl=name)
        name = steam_user.real_name
        profile_url = steam_user.profile_url
        level = steam_user.level
        xp = steam_user.xp
        content = "Your username is {0}. You have {1} friends and {2} games.".format(steam_user.name,
                                                                                     len(
                                                                                         steam_user.friends),
                                                                                     len(steam_user.games))
        img = steam_user.avatar_full
        return render_template('index.html', name=name, content=content, img=img, profile_url=profile_url, level =level,xp=xp)
    except Exception as ex:
        # We might not have permission to the user's friends list or games, so
        # just carry on with a blank message.
        return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
