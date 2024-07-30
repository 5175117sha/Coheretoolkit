'use client';

import { useLocalStorageValue } from '@react-hookz/web';
import { uniqBy } from 'lodash';
import Link from 'next/link';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import React, { useContext, useEffect, useMemo, useState } from 'react';

import { AgentSettingsForm } from '@/components/Agents//AgentSettings/AgentSettingsForm';
import { Button, Icon, Input, Text } from '@/components/Shared';
import {
  DEFAULT_AGENT_MODEL,
  DEFAULT_AGENT_TOOLS,
  DEFAULT_PREAMBLE,
  DEPLOYMENT_COHERE_PLATFORM,
  TOOL_GOOGLE_DRIVE_ID,
} from '@/constants';
import { useContextStore } from '@/context';
import { useCreateAgent, useIsAgentNameUnique, useRecentAgents } from '@/hooks/agents';
import { useNotify } from '@/hooks/toast';
import { useListTools, useOpenGoogleDrivePicker } from '@/hooks/tools';
import { DataSourceArtifact } from '@/types/tools';

const DEFAULT_FIELD_VALUES = {
  name: '',
  description: '',
  preamble: DEFAULT_PREAMBLE,
  deployment: DEPLOYMENT_COHERE_PLATFORM,
  model: DEFAULT_AGENT_MODEL,
  tools: DEFAULT_AGENT_TOOLS,
};
/**
 * @description Form to create a new agent.
 */
export const CreateAgent: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { open, close } = useContextStore();

  // const {
  //   value: pendingAssistant,
  //   set: setPendingAssistant,
  //   remove: removePendingAssistant,
  // } = useLocalStorageValue<CreateAgentFormFields>('pending_assistant', {
  //   initializeWithValue: false,
  //   defaultValue: undefined,
  // });

  const { data: toolsData } = useListTools();
  const { error } = useNotify();
  const { mutateAsync: createAgent } = useCreateAgent();
  const { addRecentAgentId } = useRecentAgents();
  const isAgentNameUnique = useIsAgentNameUnique();
  const [isSubmitting, setIsSubmitting] = useState(false);
  // const [fields, setFields] = useState<CreateAgentFormFields>(DEFAULT_FIELD_VALUES);

  const openFilePicker = useOpenGoogleDrivePicker((data) => {
    if (data.docs) {
      // setFields((prev) => {
      //   const updatedArtifacts = [
      //     ...(prev.tools_metadata?.find((tool) => tool.tool_name === TOOL_GOOGLE_DRIVE_ID)
      //       ?.artifacts ?? []),
      //     ...data.docs.map(
      //       (doc) =>
      //         ({
      //           id: doc.id,
      //           name: doc.name,
      //           type: doc.type,
      //           url: doc.url,
      //         } as DataSourceArtifact)
      //     ),
      //   ];
      //   return {
      //     ...prev,
      //     tools_metadata: [
      //       ...(prev.tools_metadata?.filter((tool) => tool.tool_name !== TOOL_GOOGLE_DRIVE_ID) ??
      //         []),
      //       ...[
      //         {
      //           tool_name: TOOL_GOOGLE_DRIVE_ID,
      //           artifacts: uniqBy(updatedArtifacts, 'id'),
      //         },
      //       ],
      //     ],
      //   };
      // });
    }
  });

  const canSubmit = (() => {
    // const { name, deployment, model } = fields;
    // const requredFields = { name, deployment, model };
    // return Object.values(requredFields).every(Boolean) && !Object.keys(fieldErrors).length;
  })();

  // const handleToolToggle = (toolName: string, checked: boolean, authUrl?: string) => {
  //   const enabledTools = [...(fields.tools ? fields.tools : [])];

  //   if (toolName === TOOL_GOOGLE_DRIVE_ID) {
  //     handleGoogleDriveToggle(checked, authUrl);
  //   }

  //   setFields((prev) => ({
  //     ...prev,
  //     tools: checked ? [...enabledTools, toolName] : enabledTools.filter((t) => t !== toolName),
  //   }));
  // };

  // const handleGoogleDriveToggle = (checked: boolean, authUrl?: string) => {
  //   const driveTool = toolsData?.find((tool) => tool.name === TOOL_GOOGLE_DRIVE_ID);
  //   if (checked) {
  //     if (driveTool?.is_auth_required && authUrl) {
  //       setPendingAssistant({
  //         ...fields,
  //         tools: [...(fields.tools ?? []), TOOL_GOOGLE_DRIVE_ID],
  //       });
  //       authUrl && window.open(authUrl, '_self');
  //     } else {
  //       openFilePicker();
  //     }
  //   } else {
  //     setFields((prev) => ({
  //       ...prev,
  //       tools: (fields.tools ?? []).filter((t) => t !== TOOL_GOOGLE_DRIVE_ID),
  //       tools_metadata: fields.tools_metadata?.filter((t) => t.tool_name !== TOOL_GOOGLE_DRIVE_ID),
  //     }));
  //   }
  // };

  // const queryString = searchParams.get('p');
  // useEffect(() => {
  //   if (queryString) {
  //     if (pendingAssistant) {
  //       setFields(pendingAssistant);
  //       removePendingAssistant();
  //     }

  //     window.history.replaceState(null, '', pathname);
  //   }
  // }, [queryString, pendingAssistant]);

  // const handleOpenSubmitModal = () => {
  //   open({
  //     title: `Create ${fields.name}?`,
  //     content: (
  //       <SubmitModalContent
  //         agentName={fields.name}
  //         onSubmit={handleSubmit}
  //         isSubmitting={isSubmitting}
  //         onClose={close}
  //       />
  //     ),
  //   });
  // };
  // const handleSubmit = async () => {
  //   if (!canSubmit) return;

  //   try {
  //     setIsSubmitting(true);

  //     const agent = await createAgent(fields);
  //     addRecentAgentId(agent.id);
  //     setFields(DEFAULT_FIELD_VALUES);
  //     close();
  //     setIsSubmitting(false);
  //     router.push(`/a/${agent.id}`);
  //   } catch (e) {
  //     setIsSubmitting(false);
  //     close();
  //     error('Failed to create assistant');
  //     console.error(e);
  //   }
  // };

  return (
    <div className="relative flex h-full w-full flex-col overflow-y-auto">
      <div className="flex flex-col space-y-5 border-b px-12 py-10 dark:border-volcanic-150">
        <div className="flex items-center space-x-2">
          <Link href="/discover">
            <Text className="dark:text-volcanic-600">All assistants</Text>
          </Link>
          <Icon name="chevron-right" className="dark:text-volcanic-600" />
          <Text className="dark:text-volcanic-600">Create assistant</Text>
        </div>
        <Text styleAs="h4">Create assistant</Text>
      </div>
      <AgentSettingsForm
        setFields={(fields) => console.log(fields)}
        handleOpenFilePicker={openFilePicker}
      />
    </div>
  );
};

const SubmitModalContent: React.FC<{
  agentName: string;
  isSubmitting: boolean;
  onSubmit: () => void;
  onClose: () => void;
}> = ({ agentName, isSubmitting, onSubmit, onClose }) => (
  <div className="flex flex-col gap-y-20">
    <Text>
      Your assistant {agentName} is about be visible publicly. Everyone in your organization will be
      able to see and use it.
    </Text>
    <div className="flex justify-between">
      <Button label="Cancel" kind="secondary" onClick={onClose} />
      <Button
        label={isSubmitting ? 'Creating assistant' : 'Yes, make it public'}
        onClick={onSubmit}
        icon="arrow-right"
        iconPosition="end"
        disabled={isSubmitting}
      />
    </div>
  </div>
);
