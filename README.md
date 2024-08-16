# Storygraph API
A python package to interact with and fetch data from the [StoryGraph](https://app.thestorygraph.com/) website.

## Features
- **Book Details**: Fetch detailed information about a book using its unique ID.
- **Search**: Perform a book search on StoryGraph and retrieve the results.
- **Fetch User lists**: 
    -  currently reading
    -  planning to read
    -  books read

## Installation
```
pip install storygraph-api
```

## Getting Started

The API is divided into two components, `Books Client` and   `User Client`.

### Book Details:

```python
# Books Client
# Fetch details of a book using its ID

from storygraph_api import Book
id = "fbdd6b7c-f512-47f2-aa94-d8bf0d5f5175"
book = Book()
result = book.book_info(id)
print(result)
```
#### Result:
```json
{
    "title": "Hagakure: The Book of the Samurai",
    "authors": [
        "Yamamoto Tsunetomo",
        "William Scott Wilson"
    ],
    "pages": "179",
    "first_pub": "1716",
    "tags": [
        "nonfiction",
        "history",
        "philosophy",
        "informative",
        "reflective",
        "slow-paced"
    ],
    "average_rating": "3.57",
    "description": "<div><em>Hagakure<\\/em> (\\\"In the Shadow of Leaves\\\") is a manual for the samurai classes consisting of a series of short anecdotes and reflections that give both insight and instruction-in the philosophy and code of behavior that foster the true spirit of Bushido-the Way of the Warrior. It is not a book of philosophy as most would understand the word: it is a collection of thoughts and sayings recorded over a period of seven years, and as such covers a wide variety of subjects, often in no particular sequence. <br><br>The work represents an attitude far removed from our modern pragmatism and materialism, and possesses an intuitive rather than rational appeal in its assertion that Bushido is a Way of Dying, and that only a samurai retainer prepared and willing to die at any moment can be totally true to his lord. While <em>Hagakure<\\/em> was for many years a secret text known only to the warrior vassals of the Hizen fief to which the author belonged, it later came to be recognized as a classic exposition of samurai thought and came to influence many subsequent generations, including Yukio Mishima. <br><br>This translation offers 300 selections that constitute the core texts of the 1,300 present in the original. <br><em>Hagakure<\\/em> was featured prominently in the film <em>Ghost Dog<\\/em>, by Jim Jarmusch.<\\/div>"
}

```


### User List:

```python
# User Client
# works only for public profiles
# fetch user's currently reading list

from storygraph_api import User
from dotenv import load_dotenv
load_dotenv()
cookie = os.getenv('COOKIE') # retrieve cookie from .env file
uname = 'sampleuname' #some username 
user = User()
result = user.currently_reading(uname,cookie=cookie)
print(result)

```

#### Result:
  
  ```json
  [
    {
        "title": "The Murder After the Night Before",
        "book_id": "38cb5b56-23f1-48fd-b4b3-a80e07a19775"
    },
    {
        "title": "The Graces",
        "book_id": "653b54b3-a79d-4c2e-ae40-eae281a91315"
    }
]

  ```

## Further Information 
*  Refer to [books_client.py](https://github.com/ym496/storygraph-api/tree/main/storygraph_api/books_client.py) and [users_client.py](https://github.com/ym496/storygraph-api/tree/main/storygraph_api/users_client.py) files to know more functionalities.
*  All the user related tasks require the `remember_user_token` cookie. It can be found in the `Application` section of your browser’s developer tools for the StoryGraph website.

## Contributing
Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

For bugs or feature requests, please open an issue on [GitHub](https://github.com/ym496/storygraph-api/issues).

## License

This project is licensed under the MIT License.
