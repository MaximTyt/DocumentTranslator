const extension = ['txt', 'doc', 'docx', 'pdf', 'xls', 'xlsx'];
document.getElementById('inputFile').addEventListener('change', function(e) {
    if (extension.some((element) => element === e.target.files[0].name.split('.').pop())) {
        document.getElementById('aboutFile').removeAttribute('hidden');
        document.getElementById('fileName').textContent = document.getElementById('fileName').textContent.replace(document.getElementById('fileName').textContent, 'Имя файла: ' + e.target.files[0].name);
        document.getElementById('fileSize').textContent = document.getElementById('fileSize').textContent.replace(document.getElementById('fileSize').textContent, 'Размер файла: ' + e.target.files[0].size/1024 + 'Kb');
        document.getElementById('translate').classList.remove('file');
    }
    else{
        alert("Загрузите текстовый файл(.txt, .doc, .docx, .pdf, .xls, .xlsx)!");
    }
});            
let inval = document.getElementById('lang_scr');
let outval = document.getElementById('lang_dest');
var input_src = document.getElementById("inp_src");
var input_dest = document.getElementById("inp_dest");
input_src.addEventListener('change', function() {
    let val = input_src.value;
    for (var i=0; i<outval.options.length; i++)
    {
        let el = outval.options[i];
        if (el.value == val)
            el.setAttribute("disabled", "");
        else
            el.removeAttribute("disabled");
    }
});
input_dest.addEventListener('change', function() {
    let val = input_dest.value;
    for (var i=0; i<inval.options.length; i++)
    {
        let el = inval.options[i] 
        if (el.value == val)
            el.setAttribute("disabled", "");
        else
            el.removeAttribute("disabled");
    }                
});
const gifs = [
            "url('../static/image/loading.gif')",
            "url('../static/image/loading1.gif')",
            "url('../static/image/loading2.gif')",
            "url('../static/image/loading3.gif')",
            "url('../static/image/loading4.gif')",
            "url('../static/image/loading5.gif')"
            ];

const load_gif = document.getElementById('loading');
var a = Math.floor(Math.random() * gifs.length);
var randomGif = gifs[a];
load_gif.style.backgroundImage = randomGif; 

function preload(){
    document.getElementById('loading').style.display = 'block';
    document.getElementById('content').style.display = 'none'
};

    