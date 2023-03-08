document.getElementById('inputFile').addEventListener('change', function(e) {
    if (e.target.files[0]) {
        document.getElementById('aboutFile').removeAttribute('hidden');
        document.getElementById('fileName').textContent = document.getElementById('fileName').textContent.replace(document.getElementById('fileName').textContent, 'Имя файла: ' + e.target.files[0].name);
        document.getElementById('fileSize').textContent = document.getElementById('fileSize').textContent.replace(document.getElementById('fileSize').textContent, 'Размер файла: ' + e.target.files[0].size/1024 + 'Kb');                    
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