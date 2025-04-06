def get_foundation_model(self, model_identifier):
    """
    Get details about an Amazon Bedrock foundation model.

    :return: The foundation model's details.
    """

    try:
        return self.bedrock_client.get_foundation_model(
            modelIdentifier=model_identifier
        )["modelDetails"]
    except ClientError:
        logger.error(
            f"Couldn't get foundation models details for {model_identifier}"
        )
        raise

def list_foundation_models(self):
    """
    List the available Amazon Bedrock foundation models.

    :return: The list of available bedrock foundation models.
    """

    try:
        response = self.bedrock_client.list_foundation_models()
        models = response["modelSummaries"]
        logger.info("Got %s foundation models.", len(models))
        return models

    except ClientError:
        logger.error("Couldn't list foundation models.")
        raise

def list_agents(self):
    """
    List the available Amazon Bedrock Agents.

    :return: The list of available bedrock agents.
    """

    try:
        all_agents = []

        paginator = self.client.get_paginator("list_agents")
        for page in paginator.paginate(PaginationConfig={"PageSize": 10}):
            all_agents.extend(page["agentSummaries"])

    except ClientError as e:
        logger.error(f"Couldn't list agents. {e}")
        raise
    else:
        return all_agents
    
def prepare_agent(self, agent_id):
    """
    Creates a DRAFT version of the agent that can be used for internal testing.

    :param agent_id: The unique identifier of the agent to prepare.
    :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
    """
    try:
        prepared_agent_details = self.client.prepare_agent(agentId=agent_id)
    except ClientError as e:
        logger.error(f"Couldn't prepare agent. {e}")
        raise
    else:
        return prepared_agent_details