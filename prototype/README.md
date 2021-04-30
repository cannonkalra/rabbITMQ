# rabbITMQ Prototype Stack
Bring the __rabbITMQ__ stack with basic level of security for quick prototyping.

## Configuration

1. Begin by changing the environment variables of each of the components of the stack.

    __NOTE__: _RabbitMQ__ devs do not consider it best practice to setup the broker via environment variables hence changes to it can be adapted via its respective configuration file (`rabbitmq.conf`)

2. Adapt changes to `rabbitmq.conf` for broker
3. Adapt changes to `telegraf.toml` file in order to change any other form of metric collection as well as incoming payload from the IoT sensors e.g. `json` or `influx` etc.

## Bringing the Stack up

    docker-compose -f docker-compose.prototype.yml up

add `-d` above if you wish to detach the logs

## Adding User Credentials for `telegraf`

`telegraf` as a consumer does not have any user credentials to obtain metrics and incoming MQTT payload from the broker, hence on needs to create these credentials.

As a result of this the `service` will keep on failing initially.

### Steps

1. Once the stack is up, head to `http://localhost:15672` and enter your brokers default user and password provided by you in `rabbitmq.conf`

2. Once logged in, head to the __Admin__ tab in the UI.

    ![RabbitMQ_Admin_UI](../.github/images/rabbit_admin_ui.png)

3. Click on __Add a user__ and enter the username / password according to that mentioned in the `prototype.env` and make sure to add `monitoring` tag to this user.

    ![RabbitMQ_Add_USer](../.github/images/rabbit_add_user.png)

4. give the user access to virtual hosts by clicking `telegraf` above and click on __Set Permission__ to grant access to `/` virtual host

    ![RabbitMQ_VHOST_ACCESS1](../.github/images/rabbit_vhost_access_1.png)

  
    ![RabbitMQ_VHOST_ACCESS2](../.github/images/rabbit_vhost_access_2.png)