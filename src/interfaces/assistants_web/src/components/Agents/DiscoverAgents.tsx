'use client';

import { useDeferredValue, useMemo, useState } from 'react';

import { Agent, ConversationWithoutMessages } from '@/cohere-client';
import { DiscoverAgentCard } from '@/components/Agents/DiscoverAgentCard';
import { Button, Icon, Input, Text, Tooltip } from '@/components/Shared';
import { useListAgents } from '@/hooks/agents';
import { useConversations } from '@/hooks/conversation';
import { useSession } from '@/hooks/session';
import { cn } from '@/utils';

const GROUPED_ASSISTANTS_LIMIT = 15;

const BASE_AGENTS: Array<Agent & { isBaseAgent: boolean }> = [
  {
    id: '',
    name: 'Command R+',
    description: 'Review, understand and ask questions about internal financial documents.',
    user_id: 'xxxx',
    created_at: '2021-09-01T00:00:00Z',
    updated_at: '2021-09-01T00:00:00Z',
    preamble: '',
    version: 1,
    temperature: 0.3,
    tools: [],
    model: '',
    deployment: '',
    isBaseAgent: true,
  },
];

export const DiscoverAgents = () => {
  const { data: agents = [] } = useListAgents();
  const { data: conversations = [] } = useConversations({});

  return (
    <div className="flex h-full w-full flex-grow flex-col overflow-y-auto rounded-lg border border-marble-950 bg-marble-980 md:ml-0 dark:border-volcanic-100 dark:bg-volcanic-100">
      <header
        className={cn(
          'border-b border-marble-950 bg-cover dark:border-volcanic-200',
          'px-4 py-6 md:px-9 md:py-10 lg:px-10',
          'flex items-center justify-between'
        )}
      >
        <div className="flex items-center gap-2">
          <Text styleAs="h4" className="text-volcanic-400 dark:text-mushroom-950">
            All Assistants
          </Text>
          <Tooltip label="tbd" hover size="sm">
            <Icon
              name="information"
              kind="outline"
              className="fill-volcanic-300 dark:fill-mushroom-700"
            />
          </Tooltip>
        </div>
        <Button kind="secondary" theme="default" icon="add" label="Create Assistant" href="/new" />
      </header>
      <section className="p-8">
        <CompanyAgents agents={agents.concat(BASE_AGENTS)} conversations={conversations} />
      </section>
    </div>
  );
};

const GroupAgents: React.FC<{ agents: Agent[]; title: string; subTitle: string }> = ({
  agents,
  title,
  subTitle,
}) => {
  const hasShowMore = agents.length > 3;
  const [showMore, setShowMore] = useState(false);
  const handleShowMore = () => setShowMore((prev) => !prev);
  const visibleAgents = showMore ? agents : agents.slice(0, 3);

  return (
    <section className="space-y-6">
      <header>
        <Text styleAs="h5" className="dark:text-marble-1000">
          {title}
        </Text>
        <Text className="dark:text-marble-800">{subTitle}</Text>
      </header>
      <div className="grid grid-cols-1 gap-x-4 gap-y-5 md:grid-cols-3 xl:grid-cols-4">
        {visibleAgents.map((agent) => (
          <DiscoverAgentCard key={agent.id} {...agent} />
        ))}
      </div>
      {hasShowMore && (
        <Button
          kind="secondary"
          label={showMore ? 'Show less' : 'Show more'}
          theme="marble"
          onClick={handleShowMore}
          icon="chevron-down"
          iconPosition="end"
          iconOptions={{
            className: cn('transform duration-300', {
              'rotate-180': showMore,
            }),
          }}
        />
      )}
    </section>
  );
};

const CompanyAgents: React.FC<{
  agents: Agent[];
  conversations: ConversationWithoutMessages[];
}> = ({ agents, conversations }) => {
  const [query, setQuery] = useState('');
  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value);
  const deferredQuery = useDeferredValue(query);
  const session = useSession();

  const createdByMeAgents = useMemo(
    () =>
      agents
        .filter(
          (agent) =>
            agent.user_id === session.userId &&
            agent.name.toLowerCase().includes(deferredQuery.toLowerCase())
        )
        .sort((a, b) => b.updated_at.localeCompare(a.updated_at)),
    [agents, session.userId, deferredQuery]
  );

  const filteredAgents = useMemo(
    () =>
      agents
        .filter((agent) => agent.name.toLowerCase().includes(deferredQuery.toLowerCase()))
        .sort((a, b) => b.name.toLowerCase().localeCompare(a.name.toLowerCase())),
    [agents, deferredQuery]
  );

  const recentlyUsedAgents = useMemo(
    () =>
      conversations
        .sort((a, b) => parseInt(b.updated_at) - parseInt(a.updated_at))
        .map((c) => filteredAgents.find((a) => a.id === c.agent_id))
        .filter((agent) => !!agent)
        .filter((agent, index, self) => self.findIndex((a) => a.id === agent.id) === index),
    [conversations, filteredAgents]
  );

  const mostUsedAgents = useMemo(
    () =>
      conversations.reduce((acc, c) => {
        if (!c.agent_id) {
          return acc;
        }
        if (!acc[c.agent_id]) {
          acc[c.agent_id] = 0;
        } else {
          acc[c.agent_id]++;
        }
        return acc;
      }, {} as Record<string, number>),
    [conversations]
  );

  const trendingAgents: Agent[] = useMemo(
    () =>
      Object.keys(mostUsedAgents)
        .sort((a, b) => mostUsedAgents[b] - mostUsedAgents[a])
        .map((id) => filteredAgents.find((a) => a.id === id))
        .filter((agent) => !!agent)
        .filter((agent) => agent.user_id !== session.userId),
    [mostUsedAgents, filteredAgents, session.userId]
  );

  return (
    <div className="max-w-screen-xl flex-grow overflow-y-auto">
      <div className="space-y-10">
        <Input
          placeholder="Search Assistants"
          type="text"
          onChange={handleOnChange}
          value={query}
        />
        <GroupAgents
          title="Created by me"
          subTitle="Assistants that you regularly use"
          agents={createdByMeAgents}
        />
        {agents.length >= GROUPED_ASSISTANTS_LIMIT && (
          <>
            <GroupAgents
              title="Recently used"
              subTitle="Assistants that you regularly use"
              agents={recentlyUsedAgents}
            />
            <GroupAgents
              title="Trending"
              subTitle="Most popular assistants from your company"
              agents={trendingAgents}
            />
          </>
        )}
        <GroupAgents
          title="All assistants"
          subTitle="All available assistants"
          agents={filteredAgents}
        />
      </div>
    </div>
  );
};
