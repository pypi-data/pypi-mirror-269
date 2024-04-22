# QuickRemember

One problem I frequently run into while using my computer is simply needing to write something down to remember at a later date. I always open up a txt file, add in the info, save it as something random, and most of the time it gets lost on my hard drive. So, in the interest of making it easier to remember things and prevent random txt files from showing up in arbitrary places that you don't know if you should delete, I wrote this very simple program to quickly save and recall short bits of information.

QuickRemember is a simple command line interface application for quickly remembering the simple things. Its usage is meant to sound like natural language, and is very simple to use. QuickRemember is made up of 3 parts: storing, recalling, and forgetting. Storing and recalling exist within the same `remember` command, and forgetting is in the `forget` command.

## Install

`pip install quickremember`

This is the first time I have ever distributed a package. On some Linux distros, it's discouraged to globally install a package with pip rather than the distro's package manager, so I'm considering learning how to and publishing a flatpak to keep it accessible to any distro.

## Usage

### Storing

Storing information is very easy. Simply use `remember <what to remember>`. You can pass informmation to it inside or outside of quotations. QuickRemember concatenates arguments together to form the query. Just remember you need to escape special characters in some way, the easiest being to use quotes.

For example:

```bash
remember My API key is 12345
```

and

```bash
remember "My API key is 12345"
```

produce the exact same result. But, 

```bash
remember I am cool & I like dolphins
```

and

```bash
remember "I am cool & I like dolphins"
```

most definitely do not, as in bash, the first example will fork the command and then we have a problem because I is probably not a command.

### Recalling

QuickRemember uses fuzzy searching (via `thefuzz` python package) to search for similar notes to a search query. Recalling, like storing, uses the remember keyword and is meant to be easy to use with natural language. To recall, simply add a `?` to the end of a search query. Once again, you can or don't have to use quotation marks.

```bash
remember my api key?
```

This will return the 5 closest-related "memories" in order of closeness.

You can also recall everything by simply executing `remember --everything`.

### Forgetting

If you are done with a piece of information and don't want to clutter your memroies, forgetting is easy as well, just run forget with a search query. The program will prompt for confirmation, and will then remove the memory.

```bash
forget my api key
```

You can also erase everything, but be careful because it is very permanent.

```bash
forget --everything
```

## Additional notes

QuickRemember stores everything in a plaintext file in your home (`~/.local/share/remember/data.txt`). It's not a safe place to store sensitive information as anyone with access to the system can see it. To combat this, I'm considering implementing a separate data file with encrypted information. This brings added complexity with security considerations such as secret key and data input being visible in the history, and the data output also possibly being visible in the history.

Some ways to combat this would be getting input where it does not display what you are typing, like how sudo gets password input. To keep data output secure, I could possibly directly copy it to clipboard or some sort of other way to securely give the information to the user, but I"m just not sure what the best way of doing this is.

## Potential future work

- [ ] Separate encrypted data storage
- [ ] Secure input for data and key entry
- [ ] Some search improvements 
