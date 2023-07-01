import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import ThemedImage from '@theme/ThemedImage';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Translate from '@docusaurus/Translate'
import useBaseUrl from '@docusaurus/useBaseUrl'
import Layout from '@theme/Layout';
import HomepageHeader from '@site/src/components/Home/Header';
import AboutJiangFeng from '@site/src/pages/About/jiangfeng';
import AboutWangJun from '@site/src/pages/About/wangjun';

import styles from './index.module.css';


export default function About(): JSX.Element {
  // https://hasura.io/legal/hasura-cloud-terms-of-service/
  return (
    <Layout
    title={'Terms'}
    description="Terms of service"
    >

      <main>
        <div
          style={{marginTop: '3vh', marginBottom: '0vh'}}
        >

          {/* <h1 style={{marginTop: '0vh', marginBottom: '-3vh', textAlign: 'center'}} className="hero__title">Contact Us</h1> */}
          {/* <hr  style={{marginTop: '2.8vh', marginBottom: '6vh', paddingLeft: '18vw', paddingRight: '18vw'}}/> */}

          {/* <h1 style={{marginTop: '0vh', marginBottom: '-0vh', textAlign: 'center'}} className="hero__title">Terms of Service</h1>
          <p style={{marginTop: '1vh', marginBottom: '-0vh', textAlign: 'center', marginLeft: '16vw', paddingBottom: '1vh', width: '68vw', fontSize: '120%', borderBottom: '1px solid #CCC'}} className="hero__title">Last Updated: July 1, 2023</p> */}

          <h1 style={{marginTop: '0vh', marginBottom: '-0vh', textAlign: 'left', marginLeft: '18vw'}} className="hero__title">Terms of Service of SIMPO</h1>
          <p style={{marginTop: '1.5vh', marginBottom: '-0vh', textAlign: 'left', marginLeft: '18vw', paddingBottom: '1vh', width: '68vw', fontSize: '120%', borderBottom: '1px solid #CCC'}} className="hero__title">Last Updated: July 1, 2023</p>


          <p className="hero__title" style={{marginTop: '2.8vh', marginBottom: '6vh', paddingLeft: '18vw', paddingRight: '18vw', textAlign: 'left', fontSize: '110%'}}>

            <p>
              Welcome to our cloud computing platform. To use our services,
              you must agree to the following terms and conditions. Please
              read and understand this agreement:
            </p>

            <p>
              <p>
                1. <b>User Qualification</b>: you must be 18 years old or of legal
                age in your jurisdiction to use our services.
              </p>
              <p>
                2.  <b>Registration Information</b>: when registering, you must
                provide accurate personal information, including but not
                limited to your name, address, email address, phone number,
                etc. You must ensure that your information is up-to-date and
                accurate.
              </p>
              <p>
                3. <b>Account Security</b>: your account and password are your
                personal confidential information. You must keep your account
                and password confidential and be responsible for any
                activities performed using your account and password. If you
                discover that your account or password has been stolen or
                used, you must notify us immediately.
              </p>
              <p>
                4. <b>Service Use</b>: you must comply with the platform's terms of
                service and not engage in any illegal or unethical activities
                when using our services.
              </p>
              <p>
                5. <b>User Uploaded Content</b>: you must ensure that any content
                uploaded to the platform does not have any illegal, obscene,
                unethical, harassing, threatening, defamatory, infringing, or
                commercial characteristics. We have the right to suspend,
                delete, or restrict any content uploaded by you.
              </p>
              <p>
                6. <b>Fees and Payment</b>: our services may charge a certain fee.
                You must pay all your fees on time, otherwise, we have the
                right to suspend or terminate your account.
              </p>
              <p>
                7. <b>Cancellation and Termination</b>: you can cancel your account
                at any time. We have the right to terminate your account at
                any time without prior notice to you. Once your account is
                terminated, you will no longer be able to access your account
                and related content.
              </p>
              <p>
                8. <b>Disclaimer</b>: we are not responsible for any loss or damage
                caused by your use of our services.
              </p>
              <p>
                9. <b>Applicable Law and Jurisdiction</b>: this agreement is subject
                to local law and jurisdiction, and the local court has
                jurisdiction.
              </p>
              <p>
                10. <b>Other</b>: we have the right to modify this agreement at any
                time and will first announce the modified agreement on the
                platform. By continuing to use our services, you agree to the
                amended agreement.
              </p>
            </p>

            <p>
              <b>
                <h2>
                  PLEASE NOTE:
                </h2>
              </b>

                <ul>
                  {/* <li>
                    IF YOU RELEASE YOUR BIOMODEL/DATASET/PROJECT TO PUBLIC VERSION, THESE REPOSITORY WILL BECOME AVAILABLE TO ALL OF THE OTHER SIMPO'S USERS, THEY CAN COPY AND CLONE THESE REPOSITORY TO MAKE THEIR OWN VERSION.
                  </li> */}
                  <li>
                    <p>
                    WE CANNOT GUARANTEE THE UNINTERRUPTED
                    OPERATION OF OUR SOFTWARE OR THAT IT WILL BE ERROR-FREE. WE
                    ARE CONTINUOUSLY DEVELOPING AND IMPROVING OUR PRODUCT, AND
                    SOME FEATURES MAY NOT WORK AS INTENDED. ADDITIONALLY,
                    INFORMATION LOSS MAY OCCUR, AND WE ARE NOT RESPONSIBLE FOR
                    ANY RESULTING DAMAGES.
                    </p>
                  </li>
                  <li>
                    <p>
                    IF YOU ACCESS SIMPO PLATFORM/SERVICES, YOU HAVE AGREED TO AND ACCEPTED THE PRACTICES DESCRIBED IN THIS TERMS OF SERVICE AND <a href="/Legal/privacy">PRIVACY POLICY</a>. IF YOU DO NOT AGREE WITH THESE TERMS AND OUR <a href="/Legal/privacy">PRIVACY POLICY</a>, YOU MUST NOT ACCESS SIMPO PLATFORM/SERVICES.
                    </p>
                  </li>
                  <li>
                    <p>
                    PLEASE CONFIRM THAT YOU HAVE READ AND UNDERSTOOD THE ABOVE TERMS AND CONDITIONS AND AGREE TO ABIDE BY THIS AGREEMENT.
                    </p>
                  </li>
                </ul>

              {/* </b> */}
            </p>


            {/* <p>
              Please confirm that you have read and understood the above
              terms and conditions and agree to abide by this agreement.
            </p> */}

          </p>


                {/* [AI]用户注册协议

        欢迎访问我们的云计算IT平台。为使用我们的服务，您必须同意以下条款和条件。请务必阅读并理解此协议。

        1. 用户资格
        您必须年满18岁，或在您所在地区已满法定年龄的情况下才能使用我们的服务。

        2. 注册信息
        注册时，您必须提供真实准确的个人信息，包括但不限于姓名、地址、电子邮件地址、电话号码等。您必须保证您的信息是最新、最准确的，并对信息的准确性负责。

        3. 账户安全
        您的账户和密码是您个人的保密信息。您必须对您的账户和密码保密，并对使用您的账户和密码进行的任何活动负责。如果您发现您的账户或密码被盗或使用，您必须立即通知我们。

        4. 服务使用
        您必须遵守平台的服务条款，在使用平台服务时不得从事任何非法或不道德的活动。

        5. 用户上传内容
        您必须确保任何上载到平台的内容不具有非法、淫秽、不道德、骚扰、威胁、诽谤、侵权或为商业目的等不当的特征。我们有权停止、删除、限制您上传的任何内容。

        6. 费用和付款
        我们的服务可能会收取一定的费用。您必须按时支付您的所有费用，否则我们有权暂停或终止您的账户。

        7. 取消和终止
        您可以在任何时候取消您的账户。我们有权在任何时候终止您的账户，并不需要事先通知您。一旦您的账户被终止，您将无法再次访问您的账户和相关内容。

        8. 免责声明
        我们对您使用我们的服务造成的任何损失或损害不承担任何责任。

        9. 法律适用和管辖
        此协议受本地法律管辖和解释，并且当地法院具有管辖权。

        10. 其他
        我们有权随时修改此协议，并会在平台上首次公布修改后的协议。如果您继续使用我们的服务，即表示您同意修改后的协议。

        请确认您已经阅读并理解了以上条款和条件，并同意遵守此协议。 */}




        </div>
      </main>

    </Layout>
  );
}
