---
kaynak: https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv/mevzuat/uluslararasi_mevzuat/cerceve_anlasmalari/Tanitici_Tarama/COMPUTERISATION_VAT.pdf
dosya: COMPUTERISATION_VAT.pdf
baglanti_sayfasi: arsiv/mevzuat/uluslararasi_mevzuat/AB_UYELIK_SURECI.htm
---

Taxation and Customs Union




Information Technology
     in DG TAXUD :
   Taxation systems



    DG TAXUD A3 IT systems and organisation                 1
                        Agenda
                                                   Taxation and Customs Union


• Overview
  – Taxation systems
  – Technical architecture
  – Services offered by DG TAXUD and FITS/TC
  – CIRCA (“Communication & Information
    Resource Centre”)
• Taxation systems review
  – Description
  – Project plan
  – Documentation
• Comitology


               DG TAXUD A3 IT systems and organisation                 2
Overview                                     Taxation and Customs Union




                  Overview

   Taxation systems and supporting
              environment




         DG TAXUD A3 IT systems and organisation                 3
          Taxation Systems
                                                 Taxation and Customs Union




• Already running:
  – VIES (VAT Information Exchange System) &
    VIES-on-the-Web
  – VoeS (VAT on e-Services)
  – Exchange of forms
• To come soon :
  – Tax on savings
• In the future (VIES 2):
  – B2B
  – 1SS (One Stop Shop) & VAT refund
  – New system for Exchange of forms

             DG TAXUD A3 IT systems and organisation                 4
Technical Architecture
                                        Taxation and Customs Union




    DG TAXUD A3 IT systems and organisation                 5
                   CCN/CSI (1)
                                                       Taxation and Customs Union


                         BS2000              HP UX
      MS Windows
                                                        SNA/CICS




                            CCN
AIX
                                                                    NT server




                                                             Sun Solaris
  DEC Alpha

                   GCOS 8             Pyramid SVr4


                   DG TAXUD A3 IT systems and organisation                      6
CCN/CSI (2)
                                    Taxation and Customs Union




DG TAXUD A3 IT systems and organisation                 7
           CCN/CSI (3)
                                                Taxation and Customs Union




CCN/CSI allow for :
  – Synchronous exchanges :
    • Uses: TUXEDO
    • Concerns: VIES Messages
  – Asynchronous exchanges :
    • Uses: MQSeries
    • Store-and-Forward protocol
    • Concerns: VIES Messages and Files



            DG TAXUD A3 IT systems and organisation                 8
                     CCN Mail2
                                                    Taxation and Customs Union




• Currently, LCMS (local CCN mail system) +
  webmail interface
   – Current mailboxes:
      • ECOM, VIESCLO, REC*, SERVICE, TAX-FRAUD, AUTOMATIC,
        SAVINGS-DIR, SEED, EWSE, MVSELO, ELO2ELO

• Future activities:
   – Anti-Virus & Anti-Spam: Q2/2006
   – Central Backup Service: Q2/2006
   – Phase 2 (Integration with national e-mail
     servers): Q4/2006



                DG TAXUD A3 IT systems and organisation                 9
              DG TAXUD A3
                                                 Taxation and Customs Union




• Project management & co-ordination, public
  procurement
• IT consultancy
• Feasibility study
• Functional & technical systems specification
• IT System design, development and
  maintenance
• IT system operation and support
• Provides test applications
• Co-ordination with the National
  Administrations

             DG TAXUD A3 IT systems and organisation                10
                    FITS/TC
                                                Taxation and Customs Union




• Helpdesk
• Documentation centre
• Tests of applications developed by MS
• Monitoring of applications in production
• Training




            DG TAXUD A3 IT systems and organisation                11
                   CCN/TC
                                               Taxation and Customs Union




• Helpdesk and support
• Operations of the CCN network
  including monitoring;
• Corrective ad evolutive maintenance
  (HW + SW)
• Development and test activities
• Documentation centre
• Training

           DG TAXUD A3 IT systems and organisation                12
                          Documentation
                                                                  Taxation and Customs Union




•   Entry point: DUG (Documentation User Guide): Catalogue of
    all available documentation and their field of application.
•   URL:

     – http://forum.europa.eu.int/Members/irc/taxud/Home/main?index
     –   Candidate Countries have access to the “Technical Assistance” Interest Group
•   Organized around Interest groups (IG);
     –   eg. Taxation, EMCS,…
•   Different services; eg. :
     –   Library (downloadable doc.)
     –   Directory (contact info.)
     –   Newsgroups
•   User ID and password obtained :
     –   by self-registration
     –   from IG Leader




                            DG TAXUD A3 IT systems and organisation                     13
How to register ?
                                                        Taxation and Customs Union

In order to obtain an access to the “Technical assistance" Interest
   Group, a userid should first be requested from Circa.
The access to Circa (Taxation and Customs Union bottom left of the
   list) is possible at the following address:
   http://forum.europa.eu.int
There:
   - click on the Taxation and Customs Union DG" button;
   - click on "Sign up";
   - complete the form (as precisely as possible) and validate.
DG TAXUD will then handle the request issued by the candidate
   country and provide a password.




                    DG TAXUD A3 IT systems and organisation                14
Taxation Systems Review                      Taxation and Customs Union




                       VIES

  VAT Information Exchange System




         DG TAXUD A3 IT systems and organisation                15
                               VIES
                                                       Taxation and Customs Union


• Objective: exchange of VAT information
  between tax administrations and/or between
  administrations and traders
• Legal bases:
   – 6th Directive (77/388/EEC)
   – Council Regulation (EEC) No 1798/2003
• VAT information:
   – Registration data (VAT number, trader’s name, address,…)
   – Turnover data (Amount of goods purchased by traders in
     other MS) :
       • Built from traders’ recapitulative statements
• Future activities :
   – Services to be included
   – Quality of Data (eg: 3rd MS requests)



                   DG TAXUD A3 IT systems and organisation                16
      VIES: Background (1)
                                              Taxation and Customs Union




How the VAT system works before the
 accession




          DG TAXUD A3 IT systems and organisation                17
      VIES: Background (2)
                                               Taxation and Customs Union




After the accession




           DG TAXUD A3 IT systems and organisation                18
           VIES Applications
                                                  Taxation and Customs Union




• run on different application platforms
• are used interactively or via automated
  applications
• are interconnected via the CCN (Common
  Communication Network)
• use a common API : CSI (Common System
  Interface) to use the CCN




              DG TAXUD A3 IT systems and organisation                19
               VIES: Project Plan
                                                       Taxation and Customs Union




•   Development:
    – approx. 600 man*days, taking into account :
        •   The interface to the backoffice
        •   The integration to the national infrastructure
    –   + approx. 40 man*days for JCSI components (only
        for VIES appl. developed in Java) :
•   Tests:
    – Local : approx. 300 man*days
    – Remote : approx. 300 man*days
•   => TOTAL = approx. 1200 man*days
•   Typical duration of project : 6 months for
    development + 3 months for local tests + 3 months
    for remote tests

                   DG TAXUD A3 IT systems and organisation                20
     VIES: Integration Steps (1)
                                                     Taxation and Customs Union




1.   VAT algorithms
     •   Provide to the Commission the VAT validation routines for
         VAT numbers
2.   Register
     •   CIRCA, CCN Web Portal, FITS/TC
3.   Download CSI stack and install it
     •   Available in C, COBOL and Java and for different target
         platforms
4.   Fill in VIES Phase 5 Application Configuration Form
     (ACF)
     •   ports for applications on the GW
     •   queues and services configuration
5.   Send the ACF to the FITS/TC
     •   Transmitted to CCN/TC for implementation



                 DG TAXUD A3 IT systems and organisation                21
   VIES: Integration Steps (2)
                                                   Taxation and Customs Union




5. Install CSI configuration file on AP
   •    Sent by FITS/TC

6. Define CCN Profiles :
   1.   Request for CCN Administration Facilities form to
        create CCN local administrator
   2.   Your CCN local administrator creates CCN users and
        associates CCN profiles to them




               DG TAXUD A3 IT systems and organisation                22
      VIES: Integration Steps (3)
                                                           Taxation and Customs Union




7.    Develop VIES applications
      •    A VIES Initial Application is available as an example
           (developed in C language for Linux)
8.  Prepare a test database for local testing
9.  Provide FITS/TC with valid and invalid VAT numbers for
    remote testing.
10. Provide the test data to FITS/TC at the latest with the ACF’s
11. Test applications locally
      •    A VIES Test Application is available (runs on Linux)
12. Test applications remotely :
      1.   with the FITS/TC (mandatory)
      2.   with other MS (optional)
13.   Move to production




                       DG TAXUD A3 IT systems and organisation                23
         VIES: Documents (1)
                                                    Taxation and Customs Union




• Functional specifications (VIES-FS-030) :
  – Design requirements (exchange protocols and message
    formats)
  – current version : 1.5
• Programming guide (VIES-PG-030) :
  – guidelines for using CSI when developing VIES applications
  – current version : 1.2
• Acceptance Test Specifications (VIES-ATS-
  030) :
  – tests to be performed locally and remotely
  – current version : 1.6


                DG TAXUD A3 IT systems and organisation                24
         VIES: Documents (2)
                                                    Taxation and Customs Union



   CCN documents applicable to VIES :
• Downloadable from the CCN Web Portal :
  – http://portal.ccntc.ccncsi.int:8080
• Application Configuration Guide (CCN/CSI-
  ACG-GEN-01-MARB) :
  – To help MS fill in the ACF
  – Under Download/Documentation/Development
• Software Installation Guide (CCN/CSI-SIG-*) :
  – Procedure to install the CSI stack on the AP
  – Under Download/Software/*




                DG TAXUD A3 IT systems and organisation                25
Taxation Systems Review                     Taxation and Customs Union




                      VoeS

        VAT on e-Services




        DG TAXUD A3 IT systems and organisation                26
                       VoeS
                                                 Taxation and Customs Union




• Objective: Collect and exchange VAT
  information about e-Services
  => allow Non-EU traders to register for
  VAT and manage their VAT returns
• Legal base:
  – 6th VAT Directive and Regulation 1798/2003
• Legislation coverage period to be
  extended to 31 December 2008


             DG TAXUD A3 IT systems and organisation                27
              VoeS: Project Plan
                                                      Taxation and Customs Union


Development:
   approx. 400 man*days, taking into account :
       The user interface for the NETPs
       The back office application including
       The messaging part (generation of XML files)
Tests:
   Local : approx. 100 man*days
   Remote : approx. 100 man*days
=> TOTAL = approx. 600 man*days
Typical duration of project : 6 months for development +
    1.5 month for local tests + 1.5 month for remote tests



                  DG TAXUD A3 IT systems and organisation                28
             VoeS: Documents
                                                    Taxation and Customs Union




• User Requirement Analysis :
   – Business analysis
   – current version : 4.0
• Functional Specifications :
   – current version : 6.1
   – contains examples illustrating e-services principles
• Technical Specifications
   – current version : 5.2
   – contains all the technical aspects




                DG TAXUD A3 IT systems and organisation                29
            VoeS: Documents
                                                    Taxation and Customs Union




• Acceptance Tests Specifications
   – current version : 3.0
   – Test cases description to ensure compliance with FS
     and TS
• Operational Procedures and Implementation Plan
   – current version : 4.0
   – Set of procedures applicable to the project




                DG TAXUD A3 IT systems and organisation                30
Taxation Systems Review                     Taxation and Customs Union




                       EOF

        Exchange of Forms




        DG TAXUD A3 IT systems and organisation                31
       EOF: Current System
                                                    Taxation and Customs Union


• Objective: Exchange of information via
  standard e-forms
  – Forms available on CIRCA,
    "SCAC" interest group,
    in "Library > Top > SCAC FORMS and GUIDEBOOKS >
    SCAC - FORMS"
• Legal base:
  – Council Regulation 1798/2003
• Exchange via CCNMail2
• Several domains:
  – VIES CLO
  – Fraud
  – Recovery of claims
  – Automatic exchange
  – Taxation on Savings
                DG TAXUD A3 IT systems and organisation                32
      EOF: Future System
                                               Taxation and Customs Union



• Objective: implement an e-form system
  that :
  – Uses XML for the forms data to allow the
    automatic processing of the forms;
  – Provide the MS with a form
    implementation that will allow them to
    load, edit and save the form data while
    easing the support of the different
    languages;


           DG TAXUD A3 IT systems and organisation                33
     EOF: Project Plan
                                               Taxation and Customs Union




• No development by NA
• Commission project in two phases:
  – Phase 1 - Specifications: Q3/2006
  – Phase 2 - e-form implementation:
    Q1/2007




           DG TAXUD A3 IT systems and organisation                34
       EOF: Documents
                                               Taxation and Customs Union




• SCIT 70 : E. of F. - Project Overview
• Forms to be exchanged can be found:
  "Library > TOP/ SCAC and Guidebooks /
  SCAC - FORMS".




           DG TAXUD A3 IT systems and organisation                35
Taxation Systems Review                     Taxation and Customs Union




                       TOS

       Taxation on Savings




        DG TAXUD A3 IT systems and organisation                36
      Taxation on Savings
                                                Taxation and Customs Union




• Objective: Exchange info on savings
  income from EU citizens
• Legal base: Directive 2003/48/EC of 30
  June 2003 - Entry into application : 1st
  July 2005
• Commission project plan
  – Functional Specifications: Q2/2006
  – Technical Specifications: > Q3/2006


            DG TAXUD A3 IT systems and organisation                37
        TOS: Project Plan
                                                Taxation and Customs Union




• Developments not started yet. It is
  anticipated that workload will be similar
  to those needed for VoeS.




            DG TAXUD A3 IT systems and organisation                38
         TOS: Documents
                                               Taxation and Customs Union




• Specification Documents are not ready
  yet (FS, TS, ATS).
• Powerpoint presentations focusing on
  FISC39 exchanges are available on
  Circa.
• FISC153 and FISC154, applicable for
  exchanges as from 2008 also available
  on Circa.


           DG TAXUD A3 IT systems and organisation                39
Taxation Systems Review                     Taxation and Customs Union




                       1SS

           One Stop Shop




        DG TAXUD A3 IT systems and organisation                40
       1SS (One Stop Shop)
                                                 Taxation and Customs Union




• Objective: allow EU traders to use their
  national VAT numbers to submit a harmonised
  VAT return through their own National
  Administration.
• 'Legal Base':
   – Commission Proposal COM(2004) 728 final
• Currently, EU traders have to be identified and
  make returns and payments in every MS
  where they carry out taxable transactions.



             DG TAXUD A3 IT systems and organisation                41
          1SS: Project Plan
                                                Taxation and Customs Union




No planning yet (Commission Proposal
 still under discussion in the Council).




            DG TAXUD A3 IT systems and organisation                42
         1SS: Documents
                                               Taxation and Customs Union




No documentation available.




           DG TAXUD A3 IT systems and organisation                43
                                    Taxation and Customs Union




       Comitology




DG TAXUD A3 IT systems and organisation                44
Comitology                                     Taxation and Customs Union




- SCAC (Standard Committee for
  Administrative Cooperation)
- SCIT (SCAC on Information Technology)
- FISCALIS




           DG TAXUD A3 IT systems and organisation                45
