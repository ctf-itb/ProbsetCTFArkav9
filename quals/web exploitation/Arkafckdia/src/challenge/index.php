<?php

  if (isset($_GET["debug"])) {
    highlight_file(__FILE__);
    die();
  }

  function processUpload() {
    if (!is_uploaded_file($_FILES['file']['tmp_name'])) {
      throw new Exception('Bukan file terupload');
    }

    if ($_FILES['file']['size'] > 3000) {
      throw new Exception('Ukuran file tidak boleh melebihi 3000 bytes');
    }

    $content = file_get_contents($_FILES['file']['tmp_name']);
    if (!ctype_punct(preg_replace('/\s+/', '', $content)) || !preg_match("/^[+\-<>\[\],.]*$/m", $content)) {
      throw new Exception('Isi file hanya boleh karakter brainfuck :(');
    }

    $name = $_FILES['file']['name'];
    $name = substr($name, 0, 50);
    $name = preg_replace('/[^a-zA-Z0-9_\.]/', '', $name);

    $blacklist = array('.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps', '.phar');
    $name = str_ireplace($blacklist, '', $name);

    $rand = bin2hex(random_bytes(12));
    $file = "uploads/arkav-$rand-$name";
    if (!move_uploaded_file($_FILES['file']['tmp_name'], $file)) {
      throw new Exception('Gagal upload file');
    }
    return $file;
  }

  $file = null;
  $output = null;
  $error = null;

  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // https://github.com/dotzero/brainfuck-php/blob/master/src/Brainfuck.php
    require 'brainfuck.php';
    try {
      $file = processUpload();
      $brainfuck = new Brainfuck(file_get_contents($file), 'Brainfuck', true);
      $output = $brainfuck->run(true);
    } catch (Exception $e) {
      $error = $e->getMessage();
    }
  }
?>
<!-- /?debug=ARKAV -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>Arkafckdia</title>

    <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <style>
        code {
          display: block;
          white-space: pre-wrap   
        }
        body {
          background-color: #212121;
        }

        /* https://uiverse.io/3bdel3ziz-T/short-warthog-21 */
        .containers {
          --transition: 350ms;
          --folder-W: 150px;
          --folder-H: 100px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: flex-end;
          padding: 10px;
          background: linear-gradient(to right, rgb(72, 230, 255), rgb(146, 116, 255), rgb(193, 89, 216));
          border-radius: 15px;
          box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
          height: calc(var(--folder-H) * 2.1);
          position: relative;
          width: 50%;
        }

        .folder {
          position: absolute;
          top: -20px;
          left: calc(50% - 60px);
          animation: float 2.5s infinite ease-in-out;
          transition: transform var(--transition) ease;
        }

        .folder:hover {
          transform: scale(1.05);
        }

        .folder .front-side,
        .folder .back-side {
          position: absolute;
          transition: transform var(--transition);
          transform-origin: bottom center;
        }

        .folder .back-side::before,
        .folder .back-side::after {
          content: "";
          display: block;
          background-color: white;
          opacity: 0.5;
          z-index: 0;
          width: var(--folder-W);
          height: var(--folder-H);
          position: absolute;
          transform-origin: bottom center;
          border-radius: 15px;
          transition: transform 350ms;
          z-index: 0;
        }

        .containers:hover .back-side::before {
          transform: rotateX(-5deg) skewX(5deg);
        }
        .containers:hover .back-side::after {
          transform: rotateX(-15deg) skewX(12deg);
        }

        .folder .front-side {
          z-index: 1;
        }

        .containers:hover .front-side {
          transform: rotateX(-40deg) skewX(15deg);
        }

        .folder .tip {
          background: linear-gradient(135deg, #ff9a56, #ff6f56);
          width: 80px;
          height: 20px;
          border-radius: 12px 12px 0 0;
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
          position: absolute;
          top: -10px;
          z-index: 2;
        }

        .folder .cover {
          background: linear-gradient(135deg, #ffe563, #ffc663);
          width: var(--folder-W);
          height: var(--folder-H);
          box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
          border-radius: 10px;
        }

        #filename {
          padding-top: 35px;
        }

        .custom-file-upload {
          font-size: 1.1em;
          color: #ffffff;
          text-align: center;
          background: rgba(255, 255, 255, 0.2);
          border: none;
          border-radius: 10px;
          box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
          cursor: pointer;
          transition: background var(--transition) ease;
          display: inline-block;
          width: 100%;
          padding: 10px 35px;
          position: relative;
        }

        .custom-file-upload:hover {
          background: rgba(255, 255, 255, 0.4);
        }

        .custom-file-upload input[type="file"] {
          display: none;
        }
        
        #arkav {
          background-image: linear-gradient(to right, rgb(72, 230, 255), rgb(146, 116, 255), rgb(193, 89, 216));
          color: transparent;
          background-clip: text;          
        }

        @keyframes float {
          0% {
            transform: translateY(0px);
          }

          50% {
            transform: translateY(-20px);
          }

          100% {
            transform: translateY(0px);
          }
        }
    </style>
  </head>

  <body>
    <div class="container mt-4">

      <div class="text-center text-white h1 fw-bold mb-2">
        <div class="h1 mb-2 fw-bold">
          Arkafckdia
        </div>
        <div class="h5" style="margin-bottom: 60px;">
          <span class="fw-bold">Brainfuck</span> compiler, only on <span class="fw-bold" id="arkav">Arkavidia</span>!
        </div>
      </div>
      
      <form method="POST" enctype="multipart/form-data">
        <div class="containers mx-auto">
          <div class="folder">
            <div class="front-side">
              <div class="tip"></div>
              <div class="cover text-center pt-4" id="filename" style="word-wrap: break-word"></div>
            </div>
            <div class="back-side cover"></div>
          </div>
          <label class="custom-file-upload">
            <input class="title" id="file" type="file" name="file" accept=".bf" required/>
            Upload Brainfuck (.bf)
          </label>
          <button type="submit" id="submit" class="btn btn-dark disabled mt-2 w-100">Compile!</button>
        </div>
      </form>
      <div class="card mt-3 w-50 mx-auto">
        <div class="card-header text-center">
          Contoh file Brainfuck
        </div>
        <div class="card-body p-0">
          <div class="row">
            <div class="col">
              <ul class="list-group list-group-flush">
                <li class="list-group-item"><a href="examples/hello_world.bf">Hello World!</a></li>
                <li class="list-group-item"><a href="examples/squares.bf">Bilangan Kuadrat</a></li>
              </ul>
            </div>
            <div class="col">
              <ul class="list-group list-group-flush">
                <li class="list-group-item"><a href="examples/arkav.bf">Text Arkav</a></li>
                <li class="list-group-item"><a href="examples/logo.bf">Logo Arkav</a></li>
              </ul>
            </div>
          </div>
          
        </div>
      </div>
      <div class="mt-3 w-80 mx-auto">

<?php if($output !== null): ?>
<?php if($output === ""): ?>
        <div class="card-header alert alert-danger">
          Tidak ada output atau terjadi error
        </div>
<?php else: ?>
      <div class="card">
        <div class="card-header alert alert-success mb-0">
          Output
        </div>
        <div class="card-body">
          <code><?php echo htmlspecialchars($output); ?></code>
        </div>
      </div>
<?php endif; ?>
<?php endif; ?>
<?php if($error): ?>
      <div class="alert alert-danger">
        <?php echo htmlspecialchars($error); ?>
      </div>
<?php elseif($file): ?>
      <div class="alert alert-success">
        File sukses terupload. <a href="<?php echo htmlspecialchars($file); ?>">Download</a>
      </div>
<?php endif; ?>
      </div>
    </div>
    <script>
    document.getElementById('file').addEventListener('change', function(event) {
      const fileName = event.target.files[0] ? event.target.files[0].name : "No file chosen";
      document.getElementById('filename').textContent = fileName;
      document.getElementById('submit').classList.remove("disabled");
    });
  </script>
  </body>
</html>
