const domain = 'http://localhost:8000/';

let list = document.querySelector('#list');
let listLoader = new XMLHttpRequest();

let title = document.querySelector('#title');
let price = document.querySelector('#price');
let content = document.querySelector('#content');
let id = document.querySelector('#id');
let rubricSelect = document.querySelector('#rubric'); 

let bbLoader = new XMLHttpRequest();
let bbUpdater = new XMLHttpRequest(); 
let bbDeleter = new XMLHttpRequest(); 

function listLoad() {
    listLoader.open('GET', domain + 'api/bbs/', true);
    listLoader.send();
}

function bbLoad(evt) {
    evt.preventDefault();
    bbLoader.open('GET', evt.target.href, true);
    bbLoader.send();
}
function bbDelete(evt) {
    evt.preventDefault(); 
    bbDeleter.open('DELETE', evt.target.href, true); 
    bbDeleter.send();
}

listLoader.addEventListener('readystatechange', () => {
    if (listLoader.readyState == 4) {
        if (listLoader.status == 200) {
            let data = JSON.parse(listLoader.responseText);
            let bbs = data.bbs; 
            let rubrics = data.rubrics; 
            let s = '';
            for (let i = 0; i < bbs.length; i++) {
                // let d = data[i];
                let d = bbs[i];
                let publishedDate = new Date(d.published);
                let formattedDate = publishedDate.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
                s += '<tr>';
                s += '<td>' + d.title + '</td>';
                s += '<td>' + d.price + '</td>';
                s += '<td>' + d.content + '</td>'; 
                s += '<td>' + formattedDate + '</td>';
                s += '<td> <a href="' + domain + 'api/bbs/' + d.id + '/" class="detail">Вывести</a> </td>';
                s += '<td> <a href="' + domain + 'api/bbs/' + d.id + '/" class="delete">Удалить</a> </td>';
                s += '</tr>';
            }
            list.innerHTML = '<table><tr><td><b>Title</b></td><td><b>Price</b></td><td><b>Published</b></td></tr>' + s + '</table>';

            let links = list.querySelectorAll('tr td a.detail');
            links.forEach((link) => {
                link.addEventListener('click', bbLoad);
            });

            links = list.querySelectorAll('tr td a.delete'); 
            links.forEach((link) => {
                link.addEventListener('click', bbDelete);
            });

            
            rubricSelect.innerHTML = '';
            rubrics.forEach((rubric) => {
                let option = document.createElement('option');
                option.value = rubric.id;
                option.textContent = rubric.name;
                rubricSelect.appendChild(option);
            });
        } else {
            window.alert(listLoader.statusText);
        }
    }
});

bbLoader.addEventListener('readystatechange', () => {
    if (bbLoader.readyState == 4) {
        if (bbLoader.status == 200) {
            let data = JSON.parse(bbLoader.responseText);
            title.value = data.title;
            price.value = data.price;
            content.value = data.content; 
        } else {
            window.alert(bbLoader.statusText);
        }
    }
});

bbUpdater.addEventListener('readystatechange', () => {
    if (bbUpdater.readyState == 4) {
        if ((bbUpdater.status == 200) || (bbUpdater.status == 201)) {
            listLoad();
            title.form.reset();
            price.form.reset(); 
            content.form.reset();
            rubric.form.reset();
            id.value == '';
        } else {
            window.alert(bbUpdater.statusText);
        }
    }
});

bbDeleter.addEventListener('readystatechange', () => {
    if (bbDeleter.readyState == 4) {
        if (bbDeleter.status == 204) {
            listLoad(); 
        } else {
            window.alert(bbDeleter.statusText); 
        }
    }
});

document.querySelector('#bb_form').addEventListener('submit', (evt) => {    
    evt.preventDefault();
    let vid = id.value, url, method;
    let selectedRubricId = rubricSelect.value;
    if (vid) {
        window.alert('МЫ ЗДЕСЬ!')
        url = 'api/bbs/' + vid + '/';
        method = 'PUT'; 
    } else {
        window.alert('МЫ ЗДЕСЬ!')
        url = 'api/bbs/';
        method = 'POST'; 
    }
    let data = JSON.stringify({
        id: vid,
        title: String(title.value),
        price: `${price.value}`,
        rubric: selectedRubricId, 
        // published: new Date().toISOString(),
        content: content.value
    }); 
    bbUpdater.open(method, domain + url, true);
    bbUpdater.setRequestHeader('Content-Type', 'application/json');
    bbUpdater.send(data);  
});

listLoad();
