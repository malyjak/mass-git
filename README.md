<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/malyjak/mass-git">
    <img src="LINK_TO_IMG" alt="Logo" width="200">
  </a>

  <h3 align="center">Mass Git</h3>
  <p align="center">
    <a href="https://github.com/malyjak?tab=repositories"><strong>Explore my other Repositories »</strong></a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
      	<li><a href="#supported-platforms">Supported Platforms</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#initialization">Initialization</a></li>
      </ul>
    </li>
    <li>
      <a href="#release-history">Release History</a>
    </li>
    <li>
      <a href="#meta">Meta</a>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

An initialization script to simplify creation of main CAT_EDLT projects via MassGit script.



<!-- GETTING STARTED -->
## Getting Started


### Supported Platforms

* Linux
* Windows


### Prerequisites

* Python


### Initialization

Clone this repository as:

```
git@github.com:malyjak/mass-git.git YOUR_PROJECT_NAME
cd YOUR_PROJECT_NAME
```

Add a new json into `.jsons` directory. See other jsons in this directory as an example. (Optional: Delete default jsons)

Then execute:

```
python mass_git.py
```

Follow up the command line.

In case you would like to be prompted with json selection again in the future, you can execute the script with `-c` switch to enforce json change:

```
python mass_git.py -c
```


<!-- RELEASE HISTORY -->
## Release History

* 0.0.1
    * Initial release



<!-- META -->
## Meta

Jakub Maly – malyjak@proton.me

Copyright (C) 2022 Jakub Maly. This is experimental software; see the source code for copying conditions. There is ABSOLUTELY NO WARRANTY; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the documentation for example usage.
