import React from 'react';
import './AboutUs.css';

const AboutUs = () => {
    const teamMembers = [
        {
            name: 'Abdullah Naveed',
            description: 'Contributed to all aspects of the project, including full-stack development, AI integration, and system design.',
            avatarInitials: 'AN',
            image: '../src/assets/abdullah.png',
            customStyle: { transform: 'scale(1.3)', objectPosition: 'bottom center' }
        },
        {
            name: 'Saqib Ali Butt',
            description: 'Contributed to all aspects of the project, including full-stack development, AI integration, and system design.',
            avatarInitials: 'SB',
            image: '../src/assets/saqib.png',
            customStyle: { transform: 'scale(1.5)', objectPosition: 'center 20%' }
        },
        {
            name: 'Anwar Karim',
            description: 'Contributed to all aspects of the project, including full-stack development, AI integration, and system design.',
            avatarInitials: 'AK',
            image: '../src/assets/anwar.png',
            customStyle: { transform: 'scale(1.3)', objectPosition: 'center' }
        }
    ];

    return (
        <div className="about-view">
            <h2>About Us</h2>
            <p className="subtitle">Meet the team behind EcoScout</p>

            <div className="team-cards-container">
                {teamMembers.map((member, index) => (
                    <div className="about-card" key={index}>
                        <div className={`avatar-circle ${member.image ? 'has-image' : ''}`}>
                            {member.image ? (
                                <img
                                    src={member.image}
                                    alt={member.name}
                                    className="member-image"
                                    style={member.customStyle}
                                />
                            ) : (
                                member.avatarInitials
                            )}
                        </div>
                        <h3>{member.name}</h3>
                        <p>{member.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AboutUs;
