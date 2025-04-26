import React, { useState } from 'react';
import { Tabs, Tab } from 'react-bootstrap';
import { CommentSelectData } from '../Interface';
import {areaTitles} from '../Constants';
import {MDBCol, MDBContainer, MDBRow} from 'mdb-react-ui-kit';
import {Separator} from './Utils';
import { getGPTComment } from '../API';
import { ACDescription, SCDescription } from '../Constants';


const CommentSelector: React.FC<{comments: CommentSelectData, section: string}> = ({ comments, section}) => {
  const [activeTab, setActiveTab] = useState('ac');
  const [selectedComments, setSelectedComments] = useState<string[]>([]);
  const [personalizedComments, setPersonalizedComments] = useState<string>("");
  const [generatedComment, setGeneratedComment] = useState<string|null>(null);
  const [modelType, setModelType] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [hasError, setHasError] = useState(false);

  const handleCheckboxChange = (comment: string) => {
    setSelectedComments(prevSelected => {
      if (prevSelected.includes(comment)) {
        return prevSelected.filter(selected => selected !== comment);
      } else {
        return [...prevSelected, comment];
      }
    });
  };

  const handleGenerateComment = () => {
    setIsGenerating(true);
    if (modelType != "") {
      setGeneratedComment(null)
      getGPTComment(section, modelType, selectedComments, personalizedComments)
      .then((response) => {
        setGeneratedComment(response);
        setIsGenerating(false);
      })
      .catch((err) => {
        console.error(err);
        setIsGenerating(false);
      });
    }
    else {
      setIsGenerating(false);
    };
};

  return (
    <MDBContainer>
      <MDBRow>
        <Tabs activeKey={activeTab} onSelect={(tab) => (tab && setActiveTab(tab))}>
          <Tab eventKey="s_and_c" title="S&C Modal">
            <Tabs defaultActiveKey="" id="sc-tabs">
              {comments['sc'] && Object.entries(comments['sc']).map(([area, commentsInArea]) => (
                commentsInArea.length > 0 && (
                    <Tab key={area} eventKey={area} title={areaTitles[area]}>
                    <div className="comment-list">

                    {commentsInArea.map((comment, index) => (
                      <label key={index}  className="comment-option">
                        <input
                          type="checkbox"
                          value={comment}
                          checked={selectedComments.includes(comment)}
                          onChange={() => handleCheckboxChange(comment)}
                        />
                        {comment}
                      </label>
                    ))}
                    </div>
                  </Tab>
                )
              ))}
            </Tabs>
          </Tab>
          <Tab eventKey="ac" title="AC Focus">
            <Tabs defaultActiveKey="learning_strategy_comment" id="ac-tabs">
                {comments['ac'] && Object.entries(comments['ac']).map(([area, commentsInArea]) => (
                  commentsInArea.length > 0 && (
                      <Tab key={area} eventKey={area} title={areaTitles[area]}>
                      <div className="comment-list">

                      {commentsInArea.map((comment, index) => (
                        <label key={index} className="comment-option">
                          <input
                            type="checkbox"
                            value={comment}
                            checked={selectedComments.includes(comment)}
                            onChange={() => handleCheckboxChange(comment)}
                          />
                          {comment}
                        </label>
                      ))}
                      </div>
                    </Tab>
                  )
                ))}
              </Tabs>
          </Tab>
          <Tab eventKey="report" title="Session Report">
            {comments['report'] && Object.entries(comments['report']).map(([area, commentsInArea]) => (
              <div className="comment-list">
                  {commentsInArea.map((comment, index) => (
                    <label key={index} className="comment-option">
                    <input
                      type="checkbox"
                      value={comment}
                      checked={selectedComments.includes(comment)}
                      onChange={() => handleCheckboxChange(comment)}
                    />
                    {comment}
                  </label>
                  ))}
              </div>
            ))}
          </Tab>
        </Tabs>
      </MDBRow>
      
      <br></br>
            <Separator thickness={4} />
      <br></br>
      <MDBRow>
          {generatedComment && (
          <>
          <label>以下是系統提供的評語(請作出相應的調整):</label>
          <div className='modalTextInput'>
            {generatedComment}
          </div>
          </>
          )

          }
      </MDBRow>

      <MDBRow>
            <select
            className='modalSelect'
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
          >
            <option value="">請選擇範圍</option>
            <option value="general">一般(整理個人化評語)</option>
            {section === 'social_style' && (
              <option value="social_style">待人處事風格</option>
            )}
            {section === 's_and_c' && (
              <>
              <option value="critical_thinking">{SCDescription.critical_thinking}</option>
              <option value="problem_solving">{SCDescription.problem_solving}</option>
              <option value="managing_information">{SCDescription.managing_information}</option>
              <option value="creativity_and_innovation">{SCDescription.creativity_and_innovation}</option>
              <option value="communication">{SCDescription.communication}</option>
              <option value="collaboration">{SCDescription.collaboration}</option>
              <option value="cultural_and_global_citizenship">{SCDescription.cultural_and_global_citizenship}</option>
              <option value="personal_growth_and_wellbeing">{SCDescription.personal_growth_and_wellbeing}</option>
              </>
            )}
            {section === "ac" && (
              <>
              <option value="learning_strategy">{ACDescription.learning_strategy}</option>
              <option value ="goal_setting">{ACDescription.goal_setting}</option>
              <option value="organising">{ACDescription.organising}</option>
              <option value="motivation_and_accountability">{ACDescription.motivation_and_accountability}</option>
              <option value="time_management">{ACDescription.time_management}</option>
              <option value="life_balance">{ACDescription.life_balance}</option>
              </>
            )
            }
      </select>
    </MDBRow>

      <MDBRow>
        <textarea
          value={personalizedComments}
          onChange={(e) => setPersonalizedComments(e.target.value)}
          placeholder="個人化評語"
          rows={5}
          cols={50}
        />
      </MDBRow>
      <MDBRow>
        <div style={{justifyContent:'center'}}>
          {/* <button className="modalButton" onClick={handleGenerateComment} disabled={isGenerating}> */}
          <button
            className={`modalButton ${isGenerating ? 'disabledButton' : ''}`}
            onClick={handleGenerateComment}
            disabled={isGenerating}
          >
            使用GPT</button>
        </div>
      </MDBRow>
    </MDBContainer>
  );
};

export default CommentSelector;
