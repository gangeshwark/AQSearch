# AQSearch
**(Audio Query Search)**<br />
Library to search for a query word (audio format) in a huge corpus audio file.

### Requirements:
1. [bob](https://www.idiap.ch/software/bob/) - 'ap' module specifically
2. [numpy](http://www.numpy.org/)
3. [matplotlib](http://matplotlib.org/)
4. [scipy](https://www.scipy.org/)

>```
>Note: Install Anaconda(https://www.continuum.io/downloads) for a full stack of libraries necessary for this model.
>```

### Running
To run the model:<br />
```$ python main.py -f mfcc/bnf/compare```<br /><br />

Example usage:<br />
To use the bottle neck features of the audio while performing DTW.<br />
`$ python main.py -f bnf`<br /><br />