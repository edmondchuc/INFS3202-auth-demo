from flask import Flask, render_template, url_for, session, redirect
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from datetime import datetime
from functools import wraps

import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
oauth = OAuth(app)
auth = oauth.register(
    settings.AUTH_NAME,
    client_id=settings.AUTH_CLIENT_ID,
    client_secret=settings.AUTH_CLIENT_SECRET,
    api_base_url=settings.AUTH_API_BASE_URL,
    access_token_url=settings.AUTH_ACCESS_TOKEN_URL,
    authorize_url=settings.AUTH_AUTHORIZE_URL
)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login')
def login():
    return auth.authorize_redirect(redirect_uri=settings.AUTH_CALLBACK_URL)


@app.route('/callback')
def auth_callback_handler():
    auth.authorize_access_token()
    user_info = auth.get('userinfo').json()

    session['jwt_payload'] = user_info
    session['profile'] = {
        'user_id': user_info['sub']
    }

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    params = {'redirect_uri': url_for('home', _external=True), 'client_id': settings.AUTH_CLIENT_ID}
    return redirect(settings.AUTH_LOGOUT_URL + '?' + urlencode(params))


def get_nav_links():
    links = [url_for('home'), url_for('about')]
    return links


@app.route('/')
def home():
    page_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi neque enim, aliquam ac vestibulum id, ullamcorper faucibus sem. Cras quis gravida risus, ac condimentum eros. In vehicula nibh auctor, gravida libero ac, molestie risus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec dignissim pulvinar.</p>"""
    links = get_nav_links()
    time = datetime.now()
    return render_template('page/index.html', title='Home Page', page_content=page_content, links=links, time=time)


@app.route('/about')
@require_auth
def about():
    page_content = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ac ex at purus interdum pellentesque. Curabitur ut convallis lectus, id pulvinar justo. Vivamus convallis nulla eu nibh ultricies, in rutrum turpis tempus. Aliquam id viverra nisi. Suspendisse mattis tortor arcu, id eleifend augue vehicula eu. Aliquam erat volutpat. Cras ac malesuada nisi. Fusce mauris erat, rhoncus non scelerisque eget, tempor et odio. In pharetra tempus accumsan. Phasellus sit amet rutrum est, nec sagittis sem.</p>

<p>Fusce facilisis lacus hendrerit metus ullamcorper bibendum eu ac libero. Aenean semper ligula at turpis varius, in rutrum ipsum molestie. Aliquam erat volutpat. Etiam luctus sapien nisi, quis lobortis sem venenatis ut. Praesent sit amet sodales ipsum. Praesent laoreet cursus scelerisque. Praesent volutpat augue quam.</p>

<p>Donec tempus, felis vitae cursus posuere, nibh quam iaculis risus, eget ultrices libero dui gravida lacus. Maecenas tristique ac risus sed viverra. Ut eget pellentesque magna. Pellentesque fringilla facilisis malesuada. Quisque ullamcorper lorem sed metus gravida, et dictum augue porta. Vestibulum et lobortis lectus, ut egestas felis. Vivamus vulputate a ex eu gravida. Integer facilisis nisl rhoncus, pharetra sem et, tempus nulla. Sed fermentum neque leo, a blandit mi vulputate sit amet. Proin eget tellus fringilla dolor eleifend iaculis id ullamcorper sem. Fusce accumsan sem vitae tortor faucibus placerat.</p>

<p>Morbi leo felis, viverra id ipsum vehicula, pulvinar pretium enim. Ut ultricies rhoncus nisl, vitae efficitur sapien ultricies in. Mauris sollicitudin lobortis ex ac molestie. Proin elit nisi, pretium at eleifend a, finibus quis risus. Vestibulum a mi et mauris consequat gravida. Vivamus laoreet velit cursus erat faucibus, et scelerisque mi molestie. Sed porta quam et odio tempus sagittis. Ut a lorem sed quam rhoncus vestibulum sed ut magna. Donec et facilisis arcu. Sed pellentesque lorem a metus vehicula auctor. Vivamus efficitur tortor nec augue venenatis, vitae gravida odio rutrum. Proin eu vehicula odio, quis vestibulum tellus. Morbi laoreet, sapien vel consequat egestas, ante turpis molestie massa, ut scelerisque tellus leo eu arcu. Fusce elementum ut libero a euismod.</p>

<p>Aenean eu odio id ligula imperdiet cursus non sit amet massa. Aenean eget turpis eu libero vestibulum venenatis. Praesent accumsan nisl ligula, ut pulvinar massa molestie et. Pellentesque in orci tempor, rhoncus odio non, iaculis velit. Phasellus sollicitudin elementum pulvinar. Quisque efficitur at ex non egestas. Praesent metus enim, scelerisque vel lorem a, convallis lacinia justo. Nulla sed dictum velit, sed blandit nisi. Morbi a elit tortor. Integer convallis ligula nec facilisis efficitur. Etiam rutrum mi eget venenatis iaculis. Nunc auctor gravida nulla, a vehicula nunc tempor tincidunt. Proin lorem arcu, efficitur eget dictum ut, cursus ac odio. Aliquam et lectus vel sapien porttitor congue ut at risus. Sed magna lacus, fringilla ut rhoncus vitae, pellentesque nec arcu. Etiam in dui ut augue tristique tincidunt a ac leo.</p>"""
    links = get_nav_links()
    time = datetime.now()
    return render_template('page/index.html', title='About Page', page_content=page_content, links=links, time=time)


if __name__ == '__main__':
    app.run(debug=True)
