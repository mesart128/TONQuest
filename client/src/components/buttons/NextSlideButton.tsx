import React from 'react';
import { useSwiper } from 'swiper/react';
import { mainButton, openLink, openTelegramLink } from '@telegram-apps/sdk-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const NextSlideButton = ({actionURL}) => {
    const swiper = useSwiper();
    const navigate = useNavigate();

    const onClick = () => {
        console.log('last slide', swiper.isEnd);
        if (swiper.isEnd === true) {
            openLink(actionURL);
            navigate(-1);
        } else {
            swiper.slideNext();
        }
    }

    useEffect(() => {
        return mainButton.onClick(onClick);
    }, [swiper]);
    

    useEffect(() => {
        console.log(swiper);
        mainButton.setParams({
            isVisible: true,
            text: swiper.isEnd === true ? 'Go to service' : 'Next',
        });
    }, [swiper.isEnd]);



    
    // useEffect(() => {
    //     if (swiper.isEnd) {
    //         mainButton.offClick(() => {swiper.slideNext();});
    //         mainButton.offClick(() => {openLink(actionURL);});
    //         mainButton.setParams({
    //             isVisible: true,
    //             text: 'Go',
    //         });
    //         for (let i = 0; i < 100; i++) {
    //             mainButton.onClick(() => {openLink(actionURL);});
    //             // mainButton.onClick(() => {openTelegramLink(`https://t.me/${i}`);});
    //         }
    //     }
    //     else {
    //         mainButton.offClick(() => {swiper.slideNext();});
    //         mainButton.offClick(() => {openLink(actionURL);});
    //         mainButton.setParams({
    //             isVisible: true,
    //             text: 'Next',
    //         });
    //         mainButton.onClick(() => {swiper.slideNext();})
    //     }
    // }, [swiper.isEnd]);





    // const [lastOffClick, setLastOffClick] = useState();

    // useEffect(() => {
    //     console.log(swiper.isEnd);
    //     if (swiper.isEnd) {
    //         mainButton.offClick(lastOffClick);
    //         mainButton.setParams({
    //             isVisible: true,
    //             text: 'Go',
    //         });
    //         const offClick = mainButton.onClick(() => {openLink(actionURL);});
    //         setLastOffClick(offClick);
    //     }
    //     else {
    //         mainButton.offClick(lastOffClick);
    //         mainButton.setParams({
    //             isVisible: true,
    //             text: 'Next',
    //         });
    //         const offClick = mainButton.onClick(() => {swiper.slideNext();})
    //         setLastOffClick(offClick);
    //     }
    // }, [swiper]);

    return <></>;
};

export default NextSlideButton;
