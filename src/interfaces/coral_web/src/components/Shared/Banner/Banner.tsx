import { Text } from '@/components/Shared';
import { cn } from '@/utils';

type Size = 'default' | 'sm';
export type BannerTheme = 'primary' | 'secondary' | 'success' | 'error' | 'neutral' | 'dark';

type Props = {
  theme?: BannerTheme;
  size?: Size;
  children?: React.ReactNode;
  className?: string;
};

const THEME_CLASSES: { [key in BannerTheme]: string } = {
  primary: 'border-coral-200 bg-coral-50 text-volcanic-900',
  secondary: 'border-mushroom-200 bg-mushroom-50 text-volcanic-900',
  success: 'border-success-200 bg-success-50 text-success-500',
  error: 'border-danger-200 bg-danger-50 text-danger-500',
  neutral: 'border-marble-950 bg-marble-950 text-volcanic-900',
  dark: 'border-volcanic-600 bg-volcanic-700 text-marble-1000',
};

export const Banner: React.FC<Props> = ({
  theme = 'primary',
  size = 'default',
  className = '',
  children,
}) => {
  const sizeClasses = size === 'default' ? 'py-6 px-4 md:px-6' : 'py-3 px-4';
  return (
    <Text
      as="div"
      className={cn(
        'rounded-lg border border-dashed',
        sizeClasses,
        THEME_CLASSES[theme],
        className
      )}
    >
      {children}
    </Text>
  );
};
