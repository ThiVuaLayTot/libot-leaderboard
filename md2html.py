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
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
    <link rel="stylesheet" href="https://thivualaytot.github.io/css/main.css">
    <link rel="stylesheet" href="https://thivualaytot.github.io/css/listwinner.css">
    <link rel="stylesheet" href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css">
    <link rel="icon" href="https://raw.githubusercontent.com/ThiVuaLayTot/ThiVuaLayTot.github.io/main/images/favicon.ico" type="image/x-icon">
</head>

<body>
    <header class="container">
        <div class="page-header">
		        <div class="logo">
                  <a href="https://thivualaytot.github.io" title="Thí Vua Lấy Tốt"><img src="https://raw.githubusercontent.com/ThiVuaLayTot/ThiVuaLayTot.github.io/main/images/favicon.ico" title="Thí Vua Lấy Tốt"></a>
            </div>
                  <ul class="navbar-nav">
                    <li>
                      <a href="https://thivualaytot.github.io" title="Trang chủ TVLT">Trang chủ</a>
                    </li>
                    <li>
                      <a href="https://thivualaytot.github.io/blog" title="Các bài Blog quan trọng của TVLT">Blog</a>
                    </li>
                    <li>
                      <a href="https://thivualaytot.github.io/vlogs" title="Các Video quan trọng của TVLT">Vlogs</a>
                    </li>
                    <li>
                      <a href="https://thivualaytot.github.io/webs" title="Social media links">Xã hội</a>
                    </li>
                    <li>
                      <a href="https://thivualaytot.github.io/game" title="Các trò chơi đơn giản">Games</a>
                    </li>
                    <li>
                      <a href="https://thivualaytot.github.io/list" title="Các danh sách/bảng quan trọng">Danh sách</a>
                    </li>
                    <li>
                      <a href="https://thivualaytot.github.io/team" title="Ban cán sự của TVLT">Mods</a>
                    </li>
                  </ul>
		        <div>
                <label class="mode">
                  <input type="checkbox" id="darkModeToggle">
                    <i id="moon" class="bx bxs-moon" title="Bật/Tắt chế độ tối"></i>
	                  <a href="#top"><i id="back2top" class="bx bxs-to-top" title="Trở lại đầu trang này"></i></a>
         		    </label>
		        </div>
        </div>
    </header>
"""

footer_style = """
    <div class="footer">
        <div class="footer-container">
            <div>
                <h3><a href="https://thivualaytot.github.io" title="Trang web Thí Vua Lấy Tốt">Thí Vua Lấy Tốt</a></h3>
                  <p><a href="https://thivualaytot.github.io/webs" title="Social media links">Các trang mạng</a></p>
                  <p><a href="https://thivualaytot.github.io/blog" title="Các bài Blog quan trọng của TVLT">Các Blog</a></p>
                  <p><a href="https://thivualaytot.github.io/vlogs" title="Các Video quan trọng của TVLT">Các Vlog</a></p>
                  <p><a href="https://thivualaytot.github.io/game" title="Các trò chơi đơn giản">Trò chơi</a></p>
                  <p><a href="https://thivualaytot.github.io/list" title="Các danh sách/bảng quan trọng">Danh sách</a></p>
                  <p><a href="https://thivualaytot.github.io/team" title="Ban cán sự của TVLT">Ban cán sự của TVLT</a></p>
            </div>
            <div>
                <h3><a href="https://thivualaytot.github.io/webs">Social meadia links</a></h3>
                <div class="button">
                  <a href="https://www.youtube.com/@TungJohnPlayingChess" target="_blank" title="Kênh Youtube của TungJohn"><i class="bx bxl-youtube"></i></a>
                  <a href="https://www.tiktok.com/@tungjohn2005" target="_blank" title="Tài khoản Tiktok của TungJohn"><i class="bx bxl-tiktok"></i></a>
                  <a href="https://clubs.chess.com/GkQy" target="_blank" title="Câu lạc bộ Thí Vua Lấy Tốt trên Chess.com"><img src="https://images.chesscomfiles.com/uploads/v1/user/33.862d5ff1.160x160o.578dc76c0662.png"></a>
                  <a href="https://lichess.org/team/thi-vua-lay-tot-tungjohn-playing-chess" target="_blank" title="Đội Thí Vua Lấy Tốt trên Lichess"><img src="https://thivualaytot.github.io/images/lichesslogo.png"></a></a>
                  <a href="https://www.facebook.com/TungJohn2005" target="_blank" title="Trang Facebook của TungJohn Playing Chess"><i class="bx bxl-facebook"></i></a></li>
                  <a href="https://zalo.me/g/zhrwtn779" target="_blank" title="Nhóm chat của Thí Vua Lấy Tốt trên Zalo"><img width="14" src="https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg"></a>
                  <a href="https://discord.gg/WUhW5Cs9gB" target="_blank" title="Máy chủ Discord của Thí Vua Lấy Tốt"><i class="bx bxl-discord"></i></a>
                </div>
            </div>
            <div>
                <br><br>
                  <p>Web được xây dựng bởi QTV <a href="https://thivualaytot.github.io/team#admins" title="Các quản trị viên">Đinh Hoàng Việt</a>.</p>
                  <p>Mã nguồn trên <a href="https://github.com/ThiVuaLayTot/ThiVuaLayTot.github.io" title="Mã nguồn của web trên Github"><img class="github-logo" src="https://github.com/fluidicon.png" alt="GitHub Icon"></a></p>
                  <label>
	                  <a href="#top"><i id="back2top" class="bx bxs-to-top" title="Trở lại đầu trang này"></i></a>
         		      </label>
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
