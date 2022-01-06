<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<p align="center">

  **<h2 align="center">Building a detailed flow model of acity using Domain Decomposition, Convolutional Autoencoders and Adversarial Networks</h2>**
  <a href="https://github.com/acse-hg2917/DDGAN_buildings">
  </a>


  <p align="center">
    ACSE-9 Independent Research Project 2021
    <br /> 
    MSc Applied Computational Science and Engineering <br /> Imperial College London
    <br /> 
    <!-- <a href="https://github.com/acse-2020/DDGAN_buildings"><strong>Explore the docs »</strong></a> -->
    <br />
    <!-- <a href="https://github.com/github_username/repo_name">View Demo</a> -->
    <!-- · -->
    <!-- <a href="https://github.com/github_username/repo_name/issues">Report Bug</a> -->
    <!-- · -->
    <!-- <a href="https://github.com/github_username/repo_name/issues">Request Feature</a> -->
  </p>
  <p align="center">
  <img src="diagram.png" alt="Logo" width="400" height="600">
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This project is a non-intrusive reduced order modelling (NIROM) on flows around buildings. High-fidelity representations of flows are compressed and modelled. In particular, proper orthogonal decomposition (POD) and convolutional autoencoders (CAE) are compared as methods for reducing order of the data, and an predictive adversarial network (built by Zef Wolffs) is used to predict the compressed flow representations. Domain decopmosition is applied to predict on a larger domain using subdomains. 


### Built With
This project is developed in Python. Packages scipy, numpy, matplotlib, sklearn, tensorflow, keras, vtu etc. were used (refer to requirements.txt). Training was done on Google Colab, utilizing Google's Compute Backend Engine GPU. 


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation of Convolutional Autoencoder (CAE) 

1. Clone the repo
   ```sh
   git clone https://github.com/gohannaago/DDGAN.git
   ```
2. Change directory to where the package is in the repo
    ```sh
    cd ./compression
    ```
3. Install requirements
    ```sh
    pip install -r requirements.txt
    ```
4. Install package
    ```sh
    pip install -e .
    ```


<!-- USAGE EXAMPLES -->
## Usage Examples
Jupyter Notebook with usage examples can be found in the examples folder. Please refer to the following notebooks in the folder.

* [Compression Training Example](https://github.com/gohannaago/DDGAN/blob/main/compression/Compression_trainCAE.ipynb) (with CAE) 
* Prediction Training Example (with Predictive Network)
* Prediction on full domain


<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact
Please contact to the following email when access for the project results is demanded. 

Hanna Go - hanna.go17@imperial.ac.uk / hannago2917@gmail.com
Project Link: [https://github.com/acse-hg2917/DDGAN_buildings](https://github.com/acse-hg2917/DDGAN_buildings)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
I would like to thank my supervisors Dr.Claire Heaney and Prof.Christopher Pain for giving the opportunity to investigate this topic and providing great guidance. I would also like to thank our DD-GAN group, especially Xiangqi Liu for working together on how to approach the buildings project and Zef Wolffs and Jon Tomasson for providing the WGAN and Predictive adversarial network constructions. 

* [Zeff Wollfs (Predictive Adversarial Network)](https://github.com/acse-zrw20/DD-GAN-AE)
* [Jon Tomasson (Predictive WGAN)](https://github.com/acse-jat20/DD-GAN)
* [Xiangqi Liu]()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username
