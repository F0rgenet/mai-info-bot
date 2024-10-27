import React from "react";
import { LucideIcon } from 'lucide-react';

interface IconWithTextProps {
  Icon: LucideIcon;
  text?: string;
  placeholder: string;
}

const IconWithText: React.FC<IconWithTextProps> = ({ Icon, text, placeholder }) => {
  const isTextAvailable = Boolean(text);

  return (
    <div className={`flex items-center ${isTextAvailable ? 'text-foreground' : 'text-accent-foreground'}`}>
      <Icon className={`w-4 h-4 mr-1 ${isTextAvailable ? 'text-primary' : 'text-accent-foreground'}`} />
      <span>{isTextAvailable ? text : placeholder}</span>
    </div>
  );
};

export default IconWithText;
