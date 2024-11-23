import React, {useEffect} from 'react';
import BottomMenu from '../components/BottomMenu';
import Navbar from '../components/Navbar';
import nftMonkey from '../assets/monkey.webp';
import { Lock, LockOpen } from 'lucide-react';

import Carousel from '../components/Carousel';
import one from '../assets/one.png';
import target from '../assets/target.png';
import {useDispatch, useSelector} from "react-redux";
import {fetchNft} from "../store/slices/nftSlice.ts";

export type Card = {
  title: string;
  subtitle: string;
  image: string;
  alt: string;
  status: string;
  isCompleted: boolean;
  subtasks: { subtaskId: number; isCompleted: boolean }[];
};

const NFTPage = () => {
  const dispatch = useDispatch();
  const branches = useSelector((state) => state.nft);

  useEffect(() => {
    dispatch(fetchNft());
  }, [dispatch]);

  let cards: Card[] = []
  for (let i = 0; i < branches.cards.length; i++) {
      let card = branches.cards[i].card
      console.log(card)
      let subtasks = []
      let length = card.subtasks? card.subtasks.length : 0
      for (let j = 0; j < length; j++) {
      subtasks.push({subtaskId: j, isCompleted: card.subtasks[j].isCompleted})
      }
      let status = card.received? "Received" : "In progress"
      cards.push({
      title: card.title,
      subtitle: card.subtitle,
      image: "https://i.ibb.co/Sn5KCD7/image.png",
      alt: card.alt,
      status: status,
      isCompleted: card.received,
      subtasks: subtasks
      })
  }
  const tasks_ = []
    for (let i = 0; i < cards.length; i++) {
        let for_push = {taskId: i, isCompleted: cards[i].isCompleted}
        tasks_.push(for_push)
    }
    const tasks = tasks_
  // const tasks = [
  //   { taskId: 0, isCompleted: true },
  //   { taskId: 1, isCompleted: true },
  //   { taskId: 2, isCompleted: false },
  //   { taskId: 3, isCompleted: true },
  //   { taskId: 4, isCompleted: false },
  //   { taskId: 5, isCompleted: false },
  // ];

  // const cards: Card[] = [
  //   {
  //     title: 'Connect a wallet',
  //     subtitle: 'Connect a wallet',
  //     status: 'Received',
  //     image: target,
  //     alt: 'target',
  //     isCompleted: true,
  //     subtasks: [{ subtaskId: 0, isCompleted: true }],
  //   },
  //   {
  //     title: 'Easy start (DEX)',
  //     subtitle: '3 tasks in the DEX branch',
  //     status: 'Received',
  //     image: target,
  //     alt: 'target',
  //     isCompleted: true,
  //     subtasks: [
  //       { subtaskId: 0, isCompleted: true },
  //       { subtaskId: 1, isCompleted: true },
  //       { subtaskId: 1, isCompleted: true },
  //     ],
  //   },
  //   {
  //     title: 'test_2',
  //     subtitle: 'subtitle',
  //     status: 'status',
  //     image: one,
  //     alt: 'number one',
  //     isCompleted: false,
  //     subtasks: [
  //       { subtaskId: 0, isCompleted: false },
  //       { subtaskId: 2, isCompleted: false },
  //       { subtaskId: 3, isCompleted: false },
  //     ],
  //   },
  //   {
  //     title: 'test_3',
  //     subtitle: 'subtitle',
  //     status: 'status',
  //     image: one,
  //     alt: 'number one',
  //     isCompleted: false,
  //     subtasks: [
  //       { subtaskId: 0, isCompleted: false },
  //       { subtaskId: 2, isCompleted: false },
  //       { subtaskId: 3, isCompleted: false },
  //     ],
  //   },
  //   {
  //     title: 'test_4',
  //     subtitle: 'subtitle',
  //     status: 'status',
  //     image: one,
  //     alt: 'number one',
  //     isCompleted: false,
  //     subtasks: [
  //       { subtaskId: 0, isCompleted: false },
  //       { subtaskId: 2, isCompleted: false },
  //       { subtaskId: 3, isCompleted: false },
  //     ],
  //   },
  //   {
  //     title: 'test_5',
  //     subtitle: 'subtitle',
  //     status: 'status',
  //     image: one,
  //     alt: 'number one',
  //     isCompleted: false,
  //     subtasks: [
  //       { subtaskId: 0, isCompleted: false },
  //       { subtaskId: 2, isCompleted: false },
  //       { subtaskId: 3, isCompleted: false },
  //     ],
  //   },
  // ];

  return (
    <div className="h-screen relative flex flex-col items-center min-w-[432px] w-full overflow-y-auto">
      <div className="bg-[#C3FF00] w-full h-4/5 rounded-full absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 blur-[500px]"></div>
      <div className="flex flex-col px-4 mx-auto w-full max-w-screen-md overflow-y-auto z-10">
        <Navbar />
        <div className="flex-1 mt-8 overflow-y-auto">
          <section className="max-w-md flex flex-col">
            <div className="flex items-center justify-center relative rounded-3xl">
              <div className="h-[400px] w-[400px] rounded-3xl absolute inset-0 mx-auto grid grid-cols-2 overflow-hidden shadow-[0_3px_10px_rgb(0,0,0,0.2)]">
                {tasks.map((item) => {
                  if (item.isCompleted) {
                    return (
                      <div className="h-[200px] w-[200px] flex flex-col justify-center items-center">
                        {/* <p className="font-medium">{item.taskId + 1} part</p> */}
                        {/* <LockOpen className="h-4 w-4" /> */}
                      </div>
                    );
                  } else {
                    return (
                      <div className="h-[200px] w-[200px] flex flex-col justify-center items-center bg-black/90 backdrop-blur-md">
                        <p className="font-medium">{item.taskId + 1} part</p>
                        <Lock className="h-4 w-4" />
                      </div>
                    );
                  }
                })}
              </div>
              <img
                src={nftMonkey}
                className="object-cover rounded-3xl h-[400px] w-[400px]"
              />
            </div>
            <h2 className="text-3xl font-bold mt-8 text-center text-white">
              NFT in pieces
            </h2>
            <p className="text-center text-white leading-5 mt-2 shadow-black">
              Complete the tasks below and assemble the NFT piece by piece
            </p>
            <Carousel items={cards} />
          </section>
        </div>
        <BottomMenu />
      </div>
    </div>
  );
};

export default NFTPage;
