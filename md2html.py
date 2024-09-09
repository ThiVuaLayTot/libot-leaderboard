import re
import os
import os.path
import logging
import logging.handlers
import datetime
import subprocess
import sys


css_styles = """<!DOCTYPE html>
<html lang="vi">

<head>
    <title>Bảng xếp hạng Bot Lichess</title>
    <meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<link rel="stylesheet" href="https://thivualaytot.github.io/css/main.css">
<link rel="stylesheet" href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css">
<link rel="icon" href="https://thivualaytot.github.io/images/favicon.ico" type="image/x-icon">

</head>

<body>
    <nav class="page-header">
        <div class="logo">
            <a href="https://thivualaytot.github.io"><img src="/images/favicon.ico"></a>
        </div>
        <ol class="navbar-nav">
            <li>
                <a href="https://thivualaytot.github.io"><i class="bx bxs-home"></i></a>
            </li>
            <li>
                <a href="https://thivualaytot.github.io/blog">
                    <i class="bx bxs-news"></i>Thông báo/Tin tức
                </a>
            </li>
            <li>
                <a href="https://thivualaytot.github.io/vlogs">
                    <i class="bx bx-play-circle"></i>Vlogs
                </a>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" href="https://thivualaytot.github.io/social">
                        <i class="bx bx-link"></i>Truyền thông <i class="bx bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a href="https://thivualaytot.github.io/social#social">Các tài khoản MXH của TungJohn</a>
                        <a href="https://thivualaytot.github.io/social#chat">Các đoạn chat của Thí Vua Lấy Tốt</a>
                        <a href="https://thivualaytot.github.io/social#group">Các nhóm/CLB/máy chủ của Thí Vua Lấy Tốt</a>
                    </div>
                </div>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" href="https://thivualaytot.github.io/lists" title="Các danh sách/bảng quan trọng">
                        <i class="bx bx-list-plus"></i>Danh sách/Tài liệu <i class="bx bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a href="https://thivualaytot.github.io/events">Danh sách tổng hợp các giải đấu</a>
                        <a href="https://thivualaytot.github.io/libot-leaderboard">Bảng xếp hạng các Bot trên Lichess</a>
                        <a href="https://chess.com/forum/view/quy-dinh-co-ban-cua-clb-tungjohn-playing-chess" target="_blank">Danh sách các tài khoản vi phạm</a>
                    </div>
                </div>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" href="https://thivualaytot.github.io/leaders" title="Ban cán sự của Thí Vua Lấy Tốt">
                        <i class="bx bx-shield-quarter"></i>Leaders <i class="bx bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a href="https://thivualaytot.github.io/leaders#admins">Administrators/Các Quản trị viên</a>
                        <a href="https://thivualaytot.github.io/leaders#mods">Moderators/Các điều hành viên</a>
                        <a href="https://thivualaytot.github.io/leaders#sponsors">Các nhà tài trợ/hợp tác với giải</a>
                    </div>
                </div>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" href="https://thivualaytot.github.io/contact-donate">
                        <i class="bx bx-donate-blood"></i>Liên hệ & Ủng hộ<i class="bx bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a href="https://thivualaytot.github.io/contact-donate#contact">Liên hệ</a>
                        <a href="https://thivualaytot.github.io/contact-donate#donate">Ủng hộ</a>
                    </div>
                </div>
            </li>
        </ol>
        <div>
            <label class="mode">
                <input type="checkbox" id="darkModeToggle">
                <i id="moon" class="bx bxs-moon" title="Bật/Tắt chế độ tối"></i>
            </label> 
        </div>
</nav>
"""

footer_style = """
    <div class="footer">
    <div class="footer-container">
        <div>
            <h3><strong><a href="https://thivualaytot.github.io" title="Trang web Thí Vua Lấy Tốt">Thí Vua Lấy Tốt</a></strong></h3>
            <p><a href="https://thivualaytot.github.io/social" title="Social media links">Các trang mạng/truyền thông</a></p>
            <p><a href="https://thivualaytot.github.io/blog" title="Các bài Blog quan trọng của TVLT">Các thông báo & tin tức</a></p>
            <p><a href="https://thivualaytot.github.io/vlogs" title="Các Video quan trọng của TVLT">Các Vlog</a></p>
            <p><a href="https://thivualaytot.github.io/game" title="Các trò chơi đơn giản">Các trò chơi đơn giản</a></p>
            <p><a href="https://thivualaytot.github.io/lists" title="Các danh sách/bảng quan trọng">Danh sách/Tài liệu</a></p>
            <p><a href="https://thivualaytot.github.io/leaders" title="Ban cán sự của TVLT">Ban cán sự của TVLT</a></p>
        </div>
        <div>
            <h3 align="center"><a href="https://thivualaytot.github.io/social">Các Liên Kết Mạng Xã Hội</a></h3>
            <strong><a href="https://thivualaytot.github.io/social#social">Các tài khoản mạng xã hội của TungJohn</a></strong>
            <div class="button">
                <a href="https://youtube.com/channel/UCvNW1NAWWjblgrP6JQI4MbQ" target="_blank" title="Kênh Youtube của TungJohn"><i class="bx bxl-youtube"></i></a>
                <a href="https://facebook.com/TungJohn2005" target="_blank" title="Trang Facebook của TungJohn"><i class="bx bxl-facebook"></i></a>
                <a href="https://twitch.tv/tungjohnplayingchess" target="_blank" title="Kênh Twitch của TungJohn"><i class="bx bxl-twitch"></i></a>
                <a href="https://tiktok.com/@tungjohn2005" target="_blank" title="Tài khoản Tiktok của TungJohn"><i class="bx bxl-tiktok"></i></a>
                <a href="https://chess.com/member/tungjohn2005" target="_blank" title="Tài khoản Chess.com của TungJohn"><img src="https://images.chesscomfiles.com/uploads/v1/user/33.862d5ff1.160x160o.578dc76c0662.png"></a>
                <a href="https://lichess.org/Tungjohn2005" target="_blank" title="Tài khoản Lichess của TungJohn"><img src="/images/lichesslogo.png"></a>
                <a href="https://shopee.vn/tungjohn2005" target="_blank" title="Shop cờ vua của TungJohn trên Shopee"><i class="bx bxs-shopping-bag"></i></a>
            </div>
            <hr>
            <strong><a href="https://thivualaytot.github.io/social#group">Các nhóm, câu lạc bộ, máy chủ của Thí Vua Lấy Tốt</a></strong>
            <div class="button">
                <a href="https://link.chess.com/club/0CVQh6" target="_blank"><img width="22" src="https://images.chesscomfiles.com/uploads/v1/user/33.862d5ff1.160x160o.578dc76c0662.png"></a>
                <a href="https://lichess.org/team/thi-vua-lay-tot-tungjohn-playing-chess" target="_blank" title="Đội Thí Vua Lấy Tốt trên Lichess"><img width="22" src="/images/lichesslogo.png"></a>
                <a href="https://facebook.com/groups/586909589413729" target="_blank" title="Nhóm Facebook của Thí Vua Lấy Tốt"><i class="bx bxl-facebook-circle"></i></a>
                <a href="https://discord.gg/Fc9MBSMbBM" target="_blank" title="Máy chủ Discord của Thí Vua Lấy Tốt"><i class="bx bxl-discord"></i></a>
                <a href="https://zalo.me/g/zhrwtn779" title="Nhóm chat Thí Vua Lấy Tốt trên Zalo"><img width="14" src="https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg"></a>
            </div>
        </div>
        <div>
            <br><br>
            <p>Web được xây dựng bởi <a href="https://thivualaytot.github.io/leaders#admins" title="Các quản trị viên">Quản trị viên</a>.</p>
            <p>Mã nguồn trên <a href="https://github.com/ThiVuaLayTot/ThiVuaLayTot.github.io"><i class="bx bxl-github"></i></a></p>
            <p><i>Lần cuối cập nhật nội dung: 15 giờ 44 phút, ngày 9/9/2024</i>.</p>
            <strong><a href="https://thivualaytot.github.io/contact-donate">Liên hệ & Đóng góp</a></strong>
        </div>
    </div>
</div>



    <script src="https://thivualaytot.github.io/js/main.js"></script>
</body>

</html>

"""

def generate_h1_tag(filename):
    title = os.path.splitext(filename)[0].capitalize()
    utc_datetime = datetime.datetime.utcnow()
    h1_tag = f"""<h1 align="center">Bảng xếp hạng {title}</h1>
    <p><i>Lần cuối cập nhật: {utc_datetime.hour}:{utc_datetime.minute}:{utc_datetime.second} UTC, ngày {utc_datetime.day} tháng {utc_datetime.month} năm {utc_datetime.year}</i></p>"""
    return h1_tag

def markdown_table_to_html(markdown_table):
    rows = markdown_table.strip().split('\n')
    html_table = '<table class="styled-table">\n'
    for i, row in enumerate(rows):
        if '---|---|---' in row:
            continue

        tag = 'th' if i == 0 else 'td'
        cells = re.split(r'\s*\|\s*', row)

        if len(cells) == 1 and cells[0] == '':
            continue
        
        html_table += '  <tr>\n'
        for cell in cells:
            if cell.startswith('@'):
                username = cell[1:]
                cell_content = f'<{tag}><a href="https://lichess.org/@/{username}">{cell}</a></{tag}>'
            else:
                cell_content = f'<{tag}>{cell}</{tag}>'
            html_table += f'    {cell_content}\n'
        html_table += '  </tr>\n'
    html_table += '</table>'
    return html_table

directories = ['html']

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            with open(os.path.join(directory, filename), 'r') as md_file:
                if filename not in ['chess960.md', 'threeCheck.md', 'kingOfTheHill.md', 'racingKings.md']:
                    f = filename
                elif filename in ["chess960.md"]:
                    f = "chess 960.md"
                elif filename in ["threeCheck.md"]:
                    f = "three-check.md"
                elif filename in ["kingOfTheHill.md"]:
                    f = "king of the hill.md"
                else:
                    f = "racing kings.md"
                h1_tag = generate_h1_tag(f)

                markdown_table = md_file.read()
                html_table = markdown_table_to_html(markdown_table)

                styled_html_table = css_styles + h1_tag + html_table + footer_style

                html_filename = os.path.splitext(filename)[0] + '.html'
                with open(os.path.join(directory, html_filename), 'w') as html_file:
                    html_file.write(styled_html_table)
