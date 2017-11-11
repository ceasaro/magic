import React from 'react';

function ManaOne(props) {
    const mana_attr = {
        className: 'mana ' + (parseInt(props.mana, 10)? 'a'+props.mana : props.mana)
    };

    return <i {...mana_attr}/>
}

function Mana(props) {
    let mana_filter = [];
    if (props.mana) {
        mana_filter.push(<ManaOne key={"a_" + props.mana.a} mana={props.mana.a}/>);
        for (let i = 0; i < props.mana.w; i++) {
            mana_filter.push(<ManaOne key={"w_" + i} mana={'w'}/>)
        }
        for (let i = 0; i < props.mana.u; i++) {
            mana_filter.push(<ManaOne key={"u_" + i} mana={'u'}/>)
        }
        for (let i = 0; i < props.mana.b; i++) {
            mana_filter.push(<ManaOne key={"b_" + i} mana={'b'}/>)
        }
        for (let i = 0; i < props.mana.r; i++) {
            mana_filter.push(<ManaOne key={"r_" + i} mana={'r'}/>)
        }
        for (let i = 0; i < props.mana.g; i++) {
            mana_filter.push(<ManaOne key={"g_" + i} mana={'g'}/>)
        }
    }
    return (<div className="mana-filter">{mana_filter}</div>)
    // return <h1>help</h1>
}

export default Mana;