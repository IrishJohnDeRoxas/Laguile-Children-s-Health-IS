let search_input = document.getElementById('id_search_input');
let genre_element = document.getElementsByName('genre')[0]
let result_div = document.getElementById('results');

// console.log(genre_element.value)


async function getTitle(url){
    let response = await fetch(url)
    try{
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`)
        }
        const books = await response.json()
        return books;
    }catch(error){
        return response.status
    }
    
}

function removeAllChildren(parent){
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}


search_input.addEventListener('keyup', async ()=>{

    let title = String(search_input.value);
    let genre = genre_element.value
    
    let url = new URL(`http://127.0.0.1:8000/search/${title}`);
    url.searchParams.append('page', 1)

    if (title.length > 0) { // Checks if the input is empty
        
        
        (async () => {

            const response = await getTitle(url);

            if (response !== 404) {
                let title_div = document.createElement('div'); 
                removeAllChildren(result_div)
                response['books'].forEach(book => {
                    const titleElement = document.createElement('a');
                    titleElement.href = `home/book/${book.id}`;
                    titleElement.textContent = book.title;
                    title_div.appendChild(titleElement);
                });

                result_div.appendChild(title_div);
                
            }else{
                result_div.textContent = 'no title found'
            }

        })();

    }
    else{
        removeAllChildren(result_div)
        console.log('Empty search bar')
    }
})