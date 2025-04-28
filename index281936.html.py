<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>EnglishLab</title>
    <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            font-family: 'Zen Maru Gothic', sans-serif;
            background-color: #f0f8ff;
            color: #333;
            background-image: url('background_design.png');
            background-repeat: no-repeat;
            background-position: center top;
            background-size: cover;
        }
        header {
            background-color: rgba(27, 79, 114, 0.9);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        header h1 {
            margin: 0;
            font-size: 2.8em;
        }
        header p {
            margin-top: 15px;
            font-size: 1.1em;
        }
        section {
            padding: 50px 20px;
            max-width: 900px;
            margin: auto;
            text-align: center;
        }
        section h2 {
            font-size: 2em;
            color: #145a87;
            margin-bottom: 20px;
        }
        section img {
            width: 100%;
            max-width: 700px;
            border-radius: 10px;
            margin: 20px 0;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }
        section img:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }
        p, ul {
            text-align: center;
        }
        ul {
            list-style-position: inside;
            display: inline-block;
            text-align: left;
        }
        footer {
            background-color: #eee;
            color: #555;
            text-align: center;
            padding: 30px 20px;
            font-size: 0.9em;
        }
    </style>
</head>

<body>

<header>
    <h1>EnglishLab</h1>
    <p>ここはMachiko先生の英語学習pageです</p>
</header>

<section id="students">
    <p>目標は大学合格!英検合格!</p>

    <img src="library_student.png" alt="図書館で本を探す学生のイラスト">

    <p>このアプリを使えば、大学合格に必要な英文法、英熟語、英作文、自由英作文が全て身につきます!</p>
    <p>英作文を使って英文法マスター、空所補充で頻出出る順英熟語、さらに難関国立大学や英検準1級の自由英作文がマスターできます。</p>

    <ul>
        <li>特徴1『答えが模範解答と異なっていても、英語として正しければ正解になる』</li>
        <li>特徴2『瞬時に点数が分かる』</li>
        <li>特徴3『一度解いた問題は保存できる』</li>
    </ul>

    <p>この他、随時、便利なアプリを追加していきます。</p>
</section>

<section id="app">
    <h2>英作文添削アプリ</h2>

    <div id="login">
        <h2>英作文添削アプリを使うにはパスワードを入力してください</h2>
        <input type="password" id="password" placeholder="パスワードを入力">
        <button onclick="checkPassword()">送信</button>
    </div>

    <div id="content" style="display:none;">
        <p>以下のボタンを押すと、アプリが別タブで開きます。</p>
        <a href="https://writingtest.streamlit.app/" target="_blank" style="
          display: inline-block;
          padding: 10px 20px;
          background-color: #4CAF50;
          color: white;
          text-decoration: none;
          border-radius: 5px;
          font-size: 16px;">
          アプリを開く
        </a>
    </div>

    <script>
        function checkPassword() {
            var input = document.getElementById("password").value;
            if (input === "goukaku0428") {
                document.getElementById("login").style.display = "none";
                document.getElementById("content").style.display = "block";
            } else {
                alert("パスワードが違います。ホームページに戻ります。");
                window.location.href = "index.html";
            }
        }
    </script>
</section>

<section id="contact">
    <h2>お問い合わせフォーム</h2>
    <p>質問などお問い合わせはこちらに入力して送信ボタンを押してください。</p>

    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfLb-00tsRR3HW0J_tpnqJK62e3CJbaZLHJJI5m2uyon6Uy4g/viewform?embedded=true" width="100%" height="689" frameborder="0" marginheight="0" marginwidth="0">
        読み込んでいます...
    </iframe>
</section>

<footer>
    &copy; 2025 English Buddy. All rights reserved.
</footer>

</body>
</html>
