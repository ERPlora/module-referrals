# Referral Program Module

Customer referral tracking and reward management.

## Features

- Track customer referrals with referrer and referred party details
- Generate and assign referral codes
- Monitor referral status through the lifecycle (pending, converted, rewarded, expired)
- Track whether rewards have been given to referrers
- Store contact information (name and email) for both referrer and referred
- Add notes to referral records

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Referral Program > Settings**

## Usage

Access via: **Menu > Referral Program**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/referrals/dashboard/` | Overview of referral program activity |
| Referrals | `/m/referrals/referrals/` | List and manage referral records |
| Settings | `/m/referrals/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Referral` | Referral record with referrer and referred party details, referral code, status, reward tracking, and notes |

## Permissions

| Permission | Description |
|------------|-------------|
| `referrals.view_referral` | View referrals |
| `referrals.add_referral` | Create new referrals |
| `referrals.change_referral` | Edit existing referrals |
| `referrals.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
