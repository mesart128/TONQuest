import React from 'react';
import QuestCard from "../components/cards/QuestCard.tsx";
import Navbar from "../components/Navbar.tsx";

const QuestPage = () => {
    return (
        <div className="min-h-screen relative bg-gradient-to-b from-black via-[#00a1ff] to-black flex flex-col items-center px-6">
            <Navbar />

            <div className="px-4 py-8">
                <section>
                    <h2 className="text-2xl font-bold mb-4 text-center">Welcome to Quest</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <QuestCard
                            title="Quest1"
                            description="Catch 5 fish in the pond"
                            xpReward={50}
                            isCompleted={true}
                        />
                        <QuestCard
                            title="Quest2"
                            description="Find the hidden treasure"
                            xpReward={100}
                        />
                        <QuestCard
                            title="Quest3"
                            description="Find the hidden treasure"
                            xpReward={100}
                        />
                    </div>
                </section>

                <section className="mt-8">
                    <h2 className="text-2xl font-bold mb-4">Tasks</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        Tasks
                    </div>
                </section>

                <section className="mt-8">
                    <h2 className="text-2xl font-bold mb-4">Bonuses</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        Bonuses
                    </div>
                </section>
            </div>
        </div>
    );
};

export default QuestPage;
