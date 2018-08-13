var gdoc_table = false;
var issue_table = false;
var ghfile_table = false;
var markdown_table = false;

function load_gdoc_table(){
    $.getJSON("/list/gdoc", function(result){
        if(!gdoc_table) {
            var r = new Array(), j = -1, size=result.length;
            r[++j] = '<thead>'
            r[++j] = '<tr class="header-row">';
            r[++j] = '<th width="50%">File Name</th>';
            r[++j] = '<th width="30%">Owner</th>';
            r[++j] = '<th width="20%">Type</th>';
            r[++j] = '</tr>';
            r[++j] = '</thead>'
            r[++j] = '<tbody>'
            for (var i=0; i<size; i++){
                r[++j] = '<tr><td>';
                r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                r[++j] = result[i]['title'];
                r[++j] = '</a>'
                r[++j] = '</td><td>';
                r[++j] = result[i]['owner_name'];
                r[++j] = '</td><td>';
                r[++j] = result[i]['mimetype'];
                r[++j] = '</td></tr>';
            }
            r[++j] = '</tbody>'
            $('#gdocs-master-list').html(r.join(''));
            gdoc_table = true;
        }
    });
    console.log('Finished loading Google Drive master list');
}

function load_issue_table(){
    $.getJSON("/list/issue", function(result){
        if(!isse_table) {
            var r = new Array(), j = -1, size=result.length;
            r[++j] = '<thead>'
            r[++j] = '<tr class="header-row">';
            r[++j] = '<th width="60%">Issue Name</th>';
            r[++j] = '<th width="40%">Repository</th>';
            r[++j] = '</tr>';
            r[++j] = '</thead>'
            r[++j] = '<tbody>'
            for (var i=0; i<size; i++){
                r[++j] ='<tr><td>';
                r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                r[++j] = result[i]['title'];
                r[++j] = '</a>'
                r[++j] = '</td><td>';
                r[++j] = '<a href="' + result[i]['repo_url'] + '" target="_blank">'
                r[++j] = result[i]['repo_name'];
                r[++j] = '</a>'
                r[++j] = '</td></tr>';
            }
            r[++j] = '</tbody>'
            $('#issues-master-list').html(r.join(''));
            issues_table = true;
        }
    });
    console.log('Finished loading Github issues master list');
}

function load_ghfile_table(){
    $.getJSON("/list/gghfile", function(result){
        if(!gdoc_table) {
            var r = new Array(), j = -1, size=result.length;
            r[++j] = '<thead>'
            r[++j] = '<tr class="header-row">';
            r[++j] = '<th width="60%">File Name</th>';
            r[++j] = '<th width="40%">Repository</th>';
            r[++j] = '</tr>';
            r[++j] = '</thead>'
            r[++j] = '<tbody>'
            for (var i=0; i<size; i++){
                r[++j] ='<tr><td>';
                r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                r[++j] = result[i]['title'];
                r[++j] = '</a>'
                r[++j] = '</td><td>';
                r[++j] = '<a href="' + result[i]['repo_url'] + '" target="_blank">'
                r[++j] = result[i]['repo_name'];
                r[++j] = '</a>'
                r[++j] = '</td></tr>';
            }
            r[++j] = '</tbody>'
            $('#ghfile-master-list').html(r.join(''));
            ghfile_table = true;
        }
    });
    console.log('Finished loading Github file list');
}

function load_markdown_table(){
    $.getJSON("/list/markdown", function(result){
        if(!gdoc_table) {
            var r = new Array(), j = -1, size=result.length;
            r[++j] = '<thead>'
            r[++j] = '<tr class="header-row">';
            r[++j] = '<th width="60%">Markdown File Name</th>';
            r[++j] = '<th width="40%">Repo</th>';
            r[++j] = '</tr>';
            r[++j] = '</thead>'
            r[++j] = '<tbody>'
            for (var i=0; i<size; i++){
                r[++j] ='<tr><td>';
                r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                r[++j] = result[i]['title'];
                r[++j] = '</a>'
                r[++j] = '</td><td>';
                r[++j] = '<a href="' + result[i]['repo_url'] + '" target="_blank">'
                r[++j] = result[i]['repo_name'];
                r[++j] = '</a>'
                r[++j] = '</td></tr>';
            }
            r[++j] = '</tbody>'
            $('#markdown-master-list').html(r.join(''));
            markdown_table = true;
        }
    });
    console.log('Finished loading Markdown list');
}

