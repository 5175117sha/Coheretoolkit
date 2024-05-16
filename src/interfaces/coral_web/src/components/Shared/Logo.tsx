import cx from 'classnames';

interface LogoProps {
  includeBrandName?: boolean;
  hasCustomLogo?: boolean;
  style?: 'default' | 'grayscale' | 'coral';
  className?: string;
  darkModeEnabled?: boolean;
}

export const Logo: React.FC<LogoProps> = ({
  includeBrandName = true,
  hasCustomLogo,
  className,
  style = 'default',
  darkModeEnabled,
}) => {
  if (hasCustomLogo === 'true') {
    // Modify this section to render a custom logo or text based on specific design guidelines.
    return <img src="/images/logo.png" alt="Logo" className={cx('h-full', className)} />;
  }

  return (
    <svg
      viewBox={includeBrandName ? '0 0 96 16' : '0 0 16 16'}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={cx('h-full', { 'w-24': includeBrandName, 'w-4': !includeBrandName }, className)}
    >
      {includeBrandName && (
        <path
          d="M27.0165 15.9968C29.3932 15.9968 31.4732 14.8084 32.2955 12.4092C32.4552 11.9287 32.2262 11.6094 31.7699 11.6094H30.8782C30.4671 11.6094 30.193 11.7916 30.0091 12.1802C29.3013 13.5749 28.3177 14.0764 27.0842 14.0764C24.8897 14.0764 23.5417 12.5446 23.5417 9.98569C23.5417 7.42679 24.9365 5.89499 27.0375 5.89499C28.3177 5.89499 29.369 6.44321 30.0317 7.74604C30.2381 8.13464 30.488 8.31684 30.9008 8.31684H31.7925C32.2488 8.31684 32.4777 8.02015 32.3181 7.5848C31.3587 4.97914 29.2094 3.9746 27.0165 3.9746C23.703 3.9746 21.2344 6.42064 21.2344 9.98569C21.2344 13.5507 23.5885 15.9968 27.0165 15.9968ZM86.8226 8.93439C87.1193 6.99143 88.4447 5.78051 90.2506 5.78051C92.0565 5.78051 93.4045 7.01401 93.5641 8.93439H86.8226ZM90.3425 15.9968C92.4451 15.9968 94.5477 15.0148 95.5764 12.7977C95.8279 12.2721 95.599 11.9061 95.1427 11.9061H94.2978C93.8866 11.9061 93.6351 12.0883 93.4287 12.4543C92.7434 13.6652 91.555 14.1683 90.3441 14.1683C88.2641 14.1683 86.9161 12.751 86.7565 10.4436H95.1443C95.6006 10.4436 95.8989 10.1921 95.8989 9.71158C95.807 6.12395 93.477 3.97622 90.2538 3.97622C87.0306 3.97622 84.4717 6.30777 84.4717 9.9873C84.4717 13.6668 86.9629 15.9984 90.3457 15.9984L90.3425 15.9968ZM77.0417 10.284H77.7963C78.2526 10.284 78.5041 10.0325 78.5735 9.55195C79.0088 6.46417 80.8164 6.05462 82.7383 6.14653C83.1495 6.16588 83.4865 5.84984 83.4865 5.43707V4.72922C83.4865 4.2729 83.2575 3.99718 82.8012 3.9746C81.1001 3.91011 79.5829 4.4938 78.7057 6.14653C78.6573 6.23682 78.5219 6.21264 78.5106 6.11106L78.3687 4.86466C78.3236 4.40834 78.072 4.17938 77.6141 4.17938H74.1635C73.7604 4.17938 73.4315 4.5067 73.4315 4.91142V5.30001C73.4315 5.70311 73.7588 6.03205 74.1635 6.03205H75.5808C75.9839 6.03205 76.3129 6.35937 76.3129 6.76408V9.55195C76.3129 9.95505 76.6402 10.284 77.0449 10.284H77.0417ZM73.9571 15.7694H81.1098C81.5661 15.7694 81.8418 15.4953 81.8418 15.0374V14.6488C81.8418 14.1925 81.5677 13.9168 81.1098 13.9168H79.2813C78.825 13.9168 78.5493 13.6426 78.5493 13.1847V11.927C78.5493 11.4707 78.2752 11.195 77.8173 11.195H77.0401C76.5838 11.195 76.308 11.4691 76.308 11.927V13.1847C76.308 13.641 76.0339 13.9168 75.576 13.9168H73.9539C73.4976 13.9168 73.2219 14.1909 73.2219 14.6488V15.0374C73.2219 15.4937 73.496 15.7694 73.9539 15.7694H73.9571ZM62.9185 8.93601C63.2152 6.99305 64.5406 5.78212 66.3465 5.78212C68.1524 5.78212 69.5004 7.01562 69.6601 8.93601H62.9185ZM66.4384 15.9984C68.541 15.9984 70.6436 15.0164 71.6723 12.7994C71.9239 12.2737 71.6949 11.9077 71.2386 11.9077H70.3937C69.9825 11.9077 69.731 12.0899 69.5246 12.4559C68.8393 13.6668 67.651 14.1699 66.4401 14.1699C64.36 14.1699 63.0121 12.7526 62.8524 10.4452H71.2402C71.6965 10.4452 71.9948 10.1937 71.9948 9.71319C71.9029 6.12557 69.573 3.97783 66.3498 3.97783C63.1265 3.97783 60.5676 6.30938 60.5676 9.98891C60.5676 13.6684 63.0588 16 66.4417 16L66.4384 15.9984ZM39.9981 15.9984C43.426 15.9984 45.8721 13.4621 45.8721 9.9873C45.8721 6.51255 43.426 3.97622 39.9981 3.97622C36.5701 3.97622 34.124 6.55931 34.124 9.9873C34.124 10.7871 34.2611 11.6787 34.6722 12.6607C34.8786 13.1412 35.2672 13.2089 35.6784 12.9122L36.3411 12.4317C36.6845 12.1802 36.7748 11.8835 36.6604 11.4498C36.4782 10.879 36.4314 10.3759 36.4314 9.94215C36.4314 7.54288 37.8713 5.8966 39.9964 5.8966C42.1216 5.8966 43.5615 7.51869 43.5615 9.9873C43.5615 12.4559 42.1442 14.078 40.0416 14.078C39.3096 14.078 38.6243 13.9409 37.8019 13.3234C37.4585 13.0493 37.1392 13.0041 36.7732 13.2782L36.2701 13.6443C35.859 13.9409 35.8138 14.3521 36.2008 14.673C37.3892 15.6324 38.7597 15.9984 39.9948 15.9984H39.9981ZM48.7728 15.7694H49.5274C49.9305 15.7694 50.2595 15.4421 50.2595 15.0374V9.57614C50.2595 7.26877 51.493 5.8966 53.4133 5.8966C55.1499 5.8966 56.1561 7.03981 56.1561 9.1424V15.039C56.1561 15.4421 56.4834 15.771 56.8881 15.771H57.6653C58.0684 15.771 58.3973 15.4437 58.3973 15.039V8.77638C58.3973 5.69183 56.8204 3.97783 54.147 3.97783C52.3266 3.97783 51.2511 4.72277 50.4481 5.75955C50.3868 5.83856 50.2627 5.79502 50.2627 5.69666V0.732037C50.2579 0.32732 49.9305 0 49.5274 0H48.7728C48.3697 0 48.0408 0.32732 48.0408 0.732037V15.0374C48.0408 15.4405 48.3681 15.7694 48.7728 15.7694Z"
          className={cx({
            'fill-green-700': style === 'default',
            'fill-primary-200': style === 'coral',
            'fill-volcanic-500': style === 'grayscale',
            'dark:fill-marble-100': darkModeEnabled,
          })}
        />
      )}
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M5.18375 9.52649C5.6144 9.52649 6.47106 9.50284 7.65517 9.01533C9.03504 8.44723 11.7804 7.41592 13.7607 6.35661C15.1458 5.6157 15.7529 4.63579 15.7529 3.31618C15.7529 1.48471 14.2682 0 12.4368 0H4.76324C2.13257 0 0 2.13257 0 4.76324C0 7.39392 1.99672 9.52649 5.18375 9.52649Z"
        className={cx({
          'fill-green-700': style === 'default',
          'fill-primary-200': style === 'coral',
          'fill-marble-400': style === 'grayscale',
          'dark:fill-marble-100': darkModeEnabled,
        })}
      />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M6.48047 12.8071C6.48047 11.5176 7.25678 10.3549 8.44779 9.86059L10.8644 8.85769C13.3087 7.84323 15.9991 9.63954 15.9991 12.2861C15.9991 14.3365 14.3366 15.9985 12.2862 15.998L9.6698 15.9973C7.90823 15.9968 6.48047 14.5686 6.48047 12.8071Z"
        className={cx({
          'fill-quartz-500': style === 'default',
          'fill-primary-200': style === 'coral',
          'fill-marble-400': style === 'grayscale',
          'dark:fill-marble-100': darkModeEnabled,
        })}
      />
      <path
        d="M2.74588 10.1523H2.74583C1.22935 10.1523 0 11.3817 0 12.8982V13.2538C0 14.7703 1.22935 15.9996 2.74583 15.9996H2.74588C4.26235 15.9996 5.4917 14.7703 5.4917 13.2538V12.8982C5.4917 11.3817 4.26235 10.1523 2.74588 10.1523Z"
        className={cx({
          'fill-primary-500': style === 'default',
          'fill-primary-200': style === 'coral',
          'fill-marble-400': style === 'grayscale',
          'dark:fill-marble-100': darkModeEnabled,
        })}
      />
    </svg>
  );
};
