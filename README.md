# Discount Code Synchronizer  #

Discount Code Synchronizer is a python app that synchronizes discount codes across multiple shopify stores every one hour.

## What is this repository for? ###

* **Quick summary**  
  1. Multiple shopify stores that belong to the same company have different discount codes created in them in a frequent way.  
  The goal is to have the same discount codes across all the different stores.  
  To tackle this, the script will run every hour and fetch the discount codes created in the previous hour and synchronizes them across each other.
  2. The script will first fetch all the discount codes present in each specified store in the configuration file.  
  3. Then, it will combine all these discount codes in a list and remove the duplicates, if there are any.  
  4. After that, the script will loop over the available stores, and for each one, compare the global list of the discount codes to its own.  
  5. Evnetually, If a discount code doesn't exist in that store, it will add it.  
* **Example**  
  1. Suppose we have 2 stores, Store1 and Store2  
  2. Store1 has the following list of discount codes: {Discount1, Discount2, Discount3}  
  3. Store2 has the following list of discount codes: {Discount3, Discount4, Discount5}  
  4. When we combine the two lists and remove the duplicates, we will get : {Discount1, Discount2, Discount3, Discount4, Discount5}  
  5. Then we will take Store1 and compare the global discount codes list to the ones present in that store.  
  6. Discount4 and Discount5 are not in Store1, so we add them (While we preserve the same details)  
  7. Discount1 and Discount2 are not in Store2, se we add them (While we preserve the same details)  
  
## Important rules to keep in mind:
* Any discount code originally assigned to a specific customer or group of customers will be duplicated as accessible to everyone instead
* Any discount code that was originally assigned to a specific product will be duplicated as allowed for all products instead
* Any discount code that was orignnally assigned a fixed discount instead of percentage discount **WILL NOT BE DUPLICATED**

 **Version**: 
   1.0.0

## Setup
Before proceeding with the following steps, please make sure you have python 3.7.9 installed on your machine.

### 1. Cloning the repository

Start by cloning this repo
```
git clone https://shtlrs@bitbucket.org/perifit-hardware/shopify-discount-codes.git
```

This should create a directory called **shopify-discount-codes** in the same directory where you've executed the git clone command.

### 2. Creating  the virtual environment

#### 2.1. Install virtualenv

```
pip install virtualenv
```

#### 2.2. Creating the virtual environment

```
virtualenv shopify-discount-codes
```

#### 2.3. Activating the virtual environment
```
shopify-discount-codes\Scripts\activate
```
### 3. Installing the requirements
```
cd shopify-discount-codes
pip install -r requirements.txt
```
### 4. Adding the shop credentials to the config file.
#### 4.1. Adding the config.ini file
Before we add the credentials, a file that needs to be called **config.ini** MUST be created under shopify-discount-codes\configuration
#### 4.2. Adding the different shop credentials to config.ini
* **Please note** that a pattern needs to be respected when doing this, otherwise it won't work.
* Each configuration needs to be added under a **section** and each section has its own **keys**
* Example of a config.ini file:  
  * Please check the config-example.ini file that you'll find in the root directory.

### 4. Configuring the environment variables.
Currently, we have one variable only: `EXECUTION_TIME_INTERVAL`.  
This variable needs to hold the number of hours every which the script will run.
For example, if the script runs every 3 hours, we need to set `EXECUTION_TIME_INTERVAL` to 3.

## Running the script
Once all the previous steps have been succesfully accomplished, the only thing left to run the script is the following command.

```bash
python main.py
```
**Note**: You need to be directly in the **shopify-discount-codes** folder to execute this.
### Who do I talk to? ###

* Amrou Bellalouna 
    * [Github profile link](https://github.com/shtlrs)
