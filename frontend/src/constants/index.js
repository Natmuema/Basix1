
import { Users, TrendingUp, Shield, Globe, Sparkles, } from 'lucide-react';

export const cards = [ 
            {
              icon: Users,
              title: 'Collaborative Ownership',
              description: 'Multiple stakeholders can co-own assets with automatic royalty distribution and transparent governance.'
            },
            {
              icon: TrendingUp,
              title: 'AI-Driven Pricing',
              description: 'MeTTa autonomous agents analyze market trends and community demand to optimize asset pricing dynamically.'
            },
            {
              icon: Shield,
              title: 'Verified Provenance',
              description: 'Complete ownership history and authenticity verification backed by blockchain and AI knowledge graphs.'
            },
            {
              icon: Globe,
              title: 'Phygital Assets',
              description: 'Bridge physical and digital worlds by tokenizing real-world items and experiences for global accessibility.'
            },
            {
              icon: Sparkles,
              title: 'Smart Contracts',
              description: 'Automated execution of agreements, funding thresholds, and profit distribution without intermediaries.'
            },
            {
              icon: TrendingUp,
              title: 'Global Marketplace',
              description: 'Connect local creators with international buyers through AI-enhanced discovery and cross-border transactions.'
            }
          
]

export const featuredAssets = [
   {
      id: 1,
      title: "Kenyan Coffee Collection NFT",
      type: "Phygital Asset",
      status: "Active",
      funded: 85,
      revenue: "$12,340",
      image: "https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 2,
      title: "Traditional Maasai Art Series",
      type: "IP Rights",
      status: "Funding",
      funded: 42,
      revenue: "$3,250",
      image: "https://images.pexels.com/photos/1070359/pexels-photo-1070359.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 3,
      title: "Sustainable Fashion Line",
      type: "Product Launch",
      status: "Planning",
      funded: 15,
      revenue: "$580",
      image: "https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=300"
    }
];

export const assets = [
    {
      id: '1',
      title: 'Artisan Coffee Blend #001',
      creator: 'Elena Rodriguez',
      price: '0.15 ETH',
      type: 'Phygital',
      image: 'https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=400',
      collaborators: 3,
      fundingProgress: 85,
      verified: true
    },
    {
      id: '2',
      title: 'Digital Art Collection',
      creator: 'Marcus Chen',
      price: '0.08 ETH',
      type: 'Digital',
      image: 'https://images.pexels.com/photos/1103970/pexels-photo-1103970.jpeg?auto=compress&cs=tinysrgb&w=400',
      collaborators: 7,
      fundingProgress: 92,
      verified: true
    },
    {
      id: '3',
      title: 'Handcrafted Jewelry Series',
      creator: 'Amara Singh',
      price: '0.22 ETH',
      type: 'Phygital',
      image: 'https://images.pexels.com/photos/1191531/pexels-photo-1191531.jpeg?auto=compress&cs=tinysrgb&w=400',
      collaborators: 5,
      fundingProgress: 67,
      verified: true
    },
    {
      id: '4',
      title: 'Music Album Rights',
      creator: 'Luna Sound',
      price: '0.32 ETH',
      type: 'Digital',
      image: 'https://images.pexels.com/photos/1626481/pexels-photo-1626481.jpeg?auto=compress&cs=tinysrgb&w=400',
      collaborators: 12,
      fundingProgress: 78,
      verified: true
    },
    {
      id: '5',
      title: 'Sustainable Fashion Line',
      creator: 'Green Threads Co',
      price: '0.18 ETH',
      type: 'Phygital',
      image: 'https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=400',
      collaborators: 6,
      fundingProgress: 91,
      verified: true
    },
    {
      id: '6',
      title: 'Virtual Reality Experience',
      creator: 'Metaverse Studios',
      price: '0.25 ETH',
      type: 'Digital',
      image: 'https://images.pexels.com/photos/2007647/pexels-photo-2007647.jpeg?auto=compress&cs=tinysrgb&w=400',
      collaborators: 9,
      fundingProgress: 54,
      verified: true
    }
  ];

  export const investments = [
    {
      id: 1,
      title: "Kenyan Coffee Collection NFT",
      creator: "Sarah Wanjiku",
      investment: "$5,000",
      returns: "+24.5%",
      status: "Active",
      image: "https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 2,
      title: "Traditional Maasai Art Series",
      creator: "Joseph Kiprotich",
      investment: "$3,200",
      returns: "+18.2%",
      status: "Active",
      image: "https://images.pexels.com/photos/1070359/pexels-photo-1070359.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 3,
      title: "Sustainable Fashion Line",
      creator: "Grace Auma",
      investment: "$2,500",
      returns: "+12.1%",
      status: "Growing",
      image: "https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=300"
    }
  ];

  export const opportunities = [
    {
      id: 4,
      title: "Organic Tea Plantation Tokens",
      creator: "David Mwangi",
      target: "$25,000",
      raised: "$18,500",
      backers: 47,
      timeLeft: "12 days",
      image: "https://images.pexels.com/photos/1638280/pexels-photo-1638280.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 5,
      title: "Handwoven Textile Collection",
      creator: "Mary Nyokabi",
      target: "$15,000",
      raised: "$8,200",
      backers: 23,
      timeLeft: "18 days",
      image: "https://images.pexels.com/photos/3985062/pexels-photo-3985062.jpeg?auto=compress&cs=tinysrgb&w=300"
    }
  ];

  export const fadeIn = (direction, delay) => {
    return {
      hidden: {
        y: direction === 'up' ? 40 : direction === 'down' ? -40 : 0,
        opacity: 0,
        x: direction === 'left' ? 40 : direction === 'right' ? -40 : 0,
      },
      show: {
        y: 0,
        x: 0,
        opacity: 1,
        transition: {
          type: 'tween',
          duration: 1.2,
          delay: delay,
          ease: [0.25, 0.25, 0.25, 0.75],
        },
      },
    };
  };

  export const walletData = {
    balance: {
      ada: 2450.75,
      usd: 1225.38
    },
    address: "addr1qx2fhv7rvv8q5jk3m7n8p9r0s1t2u3v4w5x6y7z8a9b0c1d2e3f4g5h6i7j8k9l0m1n2",
    transactions: [
      {
        id: 1,
        type: "receive",
        amount: 500,
        asset: "ADA",
        from: "Investment Return - Coffee NFT",
        timestamp: "2024-01-15 14:30",
        status: "completed"
      },
      {
        id: 2,
        type: "send",
        amount: 250,
        asset: "ADA",
        to: "Investment - Tea Plantation",
        timestamp: "2024-01-14 09:15",
        status: "completed"
      },
      {
        id: 3,
        type: "receive",
        amount: 1200,
        asset: "ADA",
        from: "Asset Sale - Textile Collection",
        timestamp: "2024-01-12 16:45",
        status: "completed"
      }
    ],
    tokens: [
      {
        name: "BASIX Token",
        symbol: "BASIX",
        balance: 1500,
        value: "$450.00",
        change: "+12.5%"
      },
      {
        name: "Coffee Collection NFT",
        symbol: "COFFEE",
        balance: 3,
        value: "$2,850.00",
        change: "+24.5%"
      },
      {
        name: "Kenyan Art Token",
        symbol: "KART",
        balance: 850,
        value: "$340.00",
        change: "+8.3%"
      }
    ]
  };

