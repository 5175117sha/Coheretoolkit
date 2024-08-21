import { Options } from 'react-hotkeys-hook';

type OptionsOrDependencyArray = Options | ReadonlyArray<unknown>;

export type QuickAction = {
  name: string;
  commands: string[];
  registerGlobal: boolean;
  closeDialogOnRun: boolean;
  action?: () => void;
  customView?: React.ReactNode;
};

export interface CustomHotKey extends QuickAction {
  options?: OptionsOrDependencyArray;
  dependencies?: OptionsOrDependencyArray;
}

export type HotKeyGroupOption = {
  group?: string;
  quickActions: CustomHotKey[];
};
