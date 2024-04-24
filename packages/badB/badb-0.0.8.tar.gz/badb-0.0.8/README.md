[![PyPI version](https://badge.fury.io/py/badB.svg)](https://badge.fury.io/py/badB)
# BadB
![BadB Hero image](https://github.com/Dev-Akash/BadB/assets/43779954/c9a7620c-9299-448c-bcba-0fa8b297ebc5)

A pip package to create Flask RESTful-api seamlessly with customizations using a JSON file.
With `badB` one can easily create the basic endpoints required to fullfill the needs of the developer while doing rapid-prototyping.

It comes with a lots of customization which you can do on the go just by tweaking few line in JSON file. 

Here JSON file acts like a blueprint for building the whole backend application. One can go from a simple CURD end points to adding authentication to routes of choice seamlessly.

Let's jump right into it to get started...

## Getting Started
- Installing package
```
pip install badB
```

- Once you have installed the package now you can easily access `badb` command from your terminal everywhere on system.
- Now create a folder as a dedicated space to project.
- Open the terminal at that location
- Just hit `badb` command on it.

Now you would be welcomed with the BadB wizard which will ask few questions to create the JSON file required to build the endpoints on the go. (To know more on how to answer these questions and create JSON file manually to extend capabilities read this.)

![image](https://github.com/Dev-Akash/BadB/assets/43779954/ebf5944e-b547-4130-87fa-a1b3b92d5533)

## Creating the Backend App

Once the JSON file is created or you done with manually creating it. It time to use the badass capability of ****badB****

In order to created app:
- Open the terminal in project folder
- Hit the command following command
```
badb-create-app [filename.json]
```

Yay! You just created your RESTful-api. <Br>
The folder with app name would be created, having all the required `Models` and a `app.py` file. 

## Launch your RESTful-api

To start your api just change directory to your generated app folder and run the following command.
```
python3 app.py
```
![image](https://github.com/Dev-Akash/BadB/assets/43779954/699315f4-5eeb-4cbb-9504-a2aee445df46)

## Understanding JSON file: The blueprint
So in order create backend APIs we are storing some information required to create those APIs. Here is the list of parameters and what they do:

<table>
  <tr>
    <th>Field</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>name</td>
    <td>Name of the App</td>
  </tr>
  <tr>
    <td>prefix</td>
    <td>The prefix to the api routes. Like /api/route_name</td>
  </tr>
  <tr>
    <td>secret</td>
    <td>This is the app secret used of hashing passwords</td>
  </tr>
  <tr>
    <td>schema</td>
    <td>This field contains the list of <code>tables</code> nested with the variables and there datatypes. One can manually add the constrains and checks and other attributes to these as we usually do in sqlite tables but in key-value pair where key would be name of field and value will be the type with attributes, constraints and checks</td>
  </tr>
  <tr>
    <td>auth_config</td>
    <td>
      This is an object having all the data configuration required for authetication in app such as:
      <li><code>auth</code> key when to true app will implement authentication to selected routes</li>
      <li><code>table</code> key containes the table name which will be holding data against which authentication data can be check such as a "user" table. Note: One need to add only tables defined under schema key</li>
      <li><code>email_field</code> key will contain a variable define in provide <code>table</code> for authentication above. It's the field name which will be used against to tally the username/email field provided by user during authentication</li>
      <li><code>pass_field</code> key also will contain a variable define in provide <code>table</code> for authentication above. It's the field name which will be used against to tally the password field provided by user during authentication</li>
      <li><code>auth_routes</code> key will contain object having key-value pair of <code>table</code> and the route methods on which the auth needs to be applied.</li>
    </td>
  </tr>
</table>

Here is a example file, which can be taken as a reference to start with: 
https://github.com/Dev-Akash/BadB/blob/152f0e6f9dc8506db287a6ca8d4d988dc4702c2c/badb.json#L1-L42
