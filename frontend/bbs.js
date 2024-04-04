const domain = 'http://localhost:8000/';

let list = document.querySelector('#list');
let listLoader = new XMLHttpRequest();

let title = document.querySelector('#title')
let price = document.querySelector('#price')

function listLoad() {
    listLoader.open('GET', domain + 'api/bbs/', true);
    listLoader.send();
}

listLoader.addEventListener('readystatechange', () => {
    if (listLoader.readyState == 4) {
        if (listLoader.status == 200) {
            let data = JSON.parse(listLoader.responseText);
            let s = '';
            for (let i = 0; i < data.length; i++) {
                let d = data[i];
                let publishedDate = new Date(d.published); 
                let formattedDate = publishedDate.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
                s += '<tr>';
                s += '<td>' + d.title + '</td>';
                s += '<td>' + d.price + '</td>';
                s += '<td>' + formattedDate + '</td>'; 
                s += '<td> <a href="' + domain + 'api/bbs/' + d.id + '/" class="detail">Вывести</a> </td>';
                s += '<td> <a href="' + domain + 'api/bbs/' + d.id + '/" class="delete">Удалить</a> </td>';
                s += '</tr>'; 
            }
            list.innerHTML = '<table><tr><td><b>Title</b></td><td><b>Price</b></td><td><b>Published</b></td></tr>' + s + '</table>';
        } else {
            window.alert(listLoader.statusText);
        }
    }
});

listLoad();