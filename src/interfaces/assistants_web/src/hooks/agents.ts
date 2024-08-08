import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { uniqBy } from 'lodash';
import { useMemo } from 'react';

import {
  AgentPublic,
  ApiError,
  ConversationPublic,
  CreateAgentRequest,
  UpdateAgentRequest,
  useCohereClient,
} from '@/cohere-client';
import { useConversations } from '@/hooks/conversation';

export const useListAgents = () => {
  const cohereClient = useCohereClient();
  return useQuery({
    queryKey: ['listAgents'],
    queryFn: () => cohereClient.listAgents({}),
  });
};

export const useCreateAgent = () => {
  const cohereClient = useCohereClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: CreateAgentRequest) => cohereClient.createAgent(request),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['listAgents'] });
    },
  });
};

export const useDeleteAgent = () => {
  const cohereClient = useCohereClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (request: { agentId: string }) => {
      try {
        return await cohereClient.deleteAgent(request);
      } catch (e) {
        console.error(e);
        throw e;
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['listAgents'] });
    },
  });
};

export const useAgent = ({ agentId }: { agentId?: string }) => {
  const cohereClient = useCohereClient();
  return useQuery({
    queryKey: ['agent', agentId],
    enabled: !!agentId,
    queryFn: async () => {
      try {
        if (!agentId) throw new Error('Agent ID not found');
        return await cohereClient.getAgent(agentId);
      } catch (e) {
        console.error(e);
        throw e;
      }
    },
  });
};

export const useDefaultAgent = (enabled?: boolean) => {
  const cohereClient = useCohereClient();
  return useQuery({
    queryKey: ['defaultAgent'],
    enabled: enabled,
    queryFn: async () => {
      return await cohereClient.getDefaultAgent();
    },
  });
};

/**
 * @description Returns a function to check if an agent name is unique.
 */
export const useIsAgentNameUnique = () => {
  const { data: agents } = useListAgents();
  return (name: string, omittedAgentId?: string) => {
    return agents
      ?.filter((agent) => agent.id !== omittedAgentId)
      .some((agent) => agent.name === name);
  };
};

export const useUpdateAgent = () => {
  const cohereClient = useCohereClient();
  const queryClient = useQueryClient();
  return useMutation<AgentPublic, ApiError, { request: UpdateAgentRequest; agentId: string }>({
    mutationFn: ({ request, agentId }) => cohereClient.updateAgent(request, agentId),
    onSettled: (agent) => {
      queryClient.invalidateQueries({ queryKey: ['agent', agent?.id] });
      queryClient.invalidateQueries({ queryKey: ['listAgents'] });
    },
  });
};

/**
 * @description Returns the most recently used agents.
 */
export const useRecentAgents = (limit: number = 5) => {
  const { data: agents = [] } = useListAgents();
  const { data: conversations = [] } = useConversations({});

  const sortByDate = (a: { updated_at: string }, b: { updated_at: string }) => {
    return Date.parse(b.updated_at ?? '') - Date.parse(a.updated_at ?? '');
  };

  const recentAgents = useMemo(
    () =>
      uniqBy(
        conversations.sort(sortByDate).map((conversation) => conversation.agent_id),
        'agent_id'
      )
        .map((agentId) => agents.find((agent) => agent.id === agentId))
        .filter((agent) => agent)
        .slice(0, limit),
    [conversations, agents]
  );
};
