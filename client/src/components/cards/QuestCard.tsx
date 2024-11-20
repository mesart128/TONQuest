import React from 'react';
import { ChevronRight } from 'lucide-react';

interface QuestCardProps {
    title: string;
    description?: string;
    xpReward?: number;
    isCompleted?: boolean;
    onClick?: () => void;
}

const QuestCard = ({
                       title,
                       description,
                       xpReward,
                       isCompleted = false,
                       onClick
                   }: QuestCardProps) => {
    return (
        <button
            onClick={onClick}
            className="w-full p-4 bg-primary/10 rounded-xl flex items-center justify-between gap-4 border border-primary/20 hover:bg-primary/20 transition-all"
        >
            <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${isCompleted ? 'bg-green-500' : 'bg-primary'}`} />
                <div className="text-left">
                    <h3 className="text-white font-medium">{title}</h3>
                    {description && (
                        <p className="text-gray-400 text-sm mt-1">{description}</p>
                    )}
                    {xpReward && (
                        <span className="text-primary text-xs mt-2 block">{xpReward} XP</span>
                    )}
                </div>
            </div>
            <ChevronRight className="text-gray-400" size={20} />
        </button>
    );
};

export default QuestCard;
