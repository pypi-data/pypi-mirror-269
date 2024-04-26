# AkitaCode Python Library

You can consult the documentation for this library in the [Wiki page of the official GitHub repository](https://github.com/alexamatausa/akitacode "AkitaCode GitHub repository").


## History log

### Version 2.0.5

- Fixed the error during the generation of the AKITA file. No data was imported into the protocol datablock. The protocol datablock was not blocked.

- The automatic capitalization rule is disabled when adding or modifying protocols, variables, functions, and arguments.


### Version 2.0.4

- Solved dependences of ``Messages`` module.


### Version 2.0.3

- The ``Messages`` module is added to the library that allows better management of messages sent and received between threads.

- Current implementations remain backward compatible with previous versions, since the ``Message`` superclass has a STR method.

- Status messages are added to the methods of the ``Document`` class.

- The `make()` method is added, which allows all methods of the ``Document`` class to be executed. To ensure proper compilation, we highly recommend using this method.


### Version 2.0.2

- Fixed an issue during the call to a *for* instance, where the evaluated variables were not correctly set as environment constants.

- Deleted some debug print to stdout.

- The conditions for the correct evaluation of arguments dependent on the specified environment when using a *for* instance are modified.

- Fixed an indexing error during export of functions and arguments.

- Support is added for the use of functions within "for" instances, allowing environment constants to be set as the value of the arguments.


### Version 2.0.2-beta

- Fixed problem during *for* line statement. Now, *for* statements can be used as following:
```
for each case of ( BAT_Temperature , BAT_SOH , BAT_SOC ) do
```


### Version 2.0.1

- Library dependencies have been fixed.


### Version 2.0.0

- First version.

